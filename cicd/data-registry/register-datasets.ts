const axios = require('axios');
const readline = require('readline');
const isEqual = require('lodash.isequal');

import http, {DatastoreType} from './registry-http';

// TODO need userId + customerAccountId for SCAN-COMPONENTS (for each environment)
axios.defaults.headers.common = {
    'X-netscan-UserId': 'bkuuek7dfetg027vtt80',
    'X-netscan-CustomerAccountId': 'bkuuek7dfetg027vttqg'
};

export async function registerDatasets(localDatasets: Dataset[], datastore: DatastoreType, args: any) {

    const remoteDatasets = await http.getDatasets(datastore);

    // final all that need created on remote.
    const toBeCreated = localDatasets.filter(ds => doesNotExist(ds, remoteDatasets));
    const toBeDeleted = remoteDatasets.filter(ds => doesNotExist(ds, localDatasets));
    const toBeUpdated = localDatasets.map((ds): Dataset => {
        const other = findMatch(ds, remoteDatasets);

        if (other && other.description !== ds.description) {
            return {
                ...ds,
                id: other.id
            };
        }
    }).filter(x => !!x);

    const schemaToBeUpdated$ = await Promise.all(localDatasets.map(async (ds): Promise<Dataset> => {
        const other = findMatch(ds, remoteDatasets);
        if (other) {
            const schema = await http.getSchema(other);
            if (!isEqual(schema, ds.schema)) {
                return {
                    ...ds,
                    id: other.id
                };
            }
        }
    }));

    // combine existing datasets w/ newly created datasets (they both require schema updates)
    const schemaToBeUpdated =
        schemaToBeUpdated$.filter(x => !!x);

    console.log(`TABLES IN WCAAS: ${localDatasets.length}`);
    console.log(`DATASETS CURRENTLY REGISTERED: ${remoteDatasets.length}`);

    console.log(`\nPLAN:`);
    console.log(`  WCAAS TABLES TO BE CREATED IN REGISTRY: ${toBeCreated.length}`);
    console.log(`  WCAAS TABLES TO BE DELETED IN REGISTRY: ${toBeDeleted.length}`);
    console.log(`  WCAAS TABLES TO BE UPDATED IN REGISTRY: ${toBeUpdated.length}`);
    console.log(`  WCAAS SCHEMAS TO BE UPDATED IN REGISTRY: ${schemaToBeUpdated.length + toBeCreated.length}`);

    if (!args.autoApprove && !await promptApproval()) {
        console.log("Aborting");
        return;
    }

    const createdResults = await Promise.all(toBeCreated.map(async dataset => await http.createDataset(dataset)));
    const deletedResults = await Promise.all(toBeDeleted.map(async dataset => await http.deleteDataset(dataset)));
    const updateResults = await Promise.all(toBeUpdated.map(async dataset => await http.updateDataset(dataset)));

    console.log(`\nAPPLY:`)
    console.log(`  WCAAS TABLES CREATED IN REGISTRY: ${createdResults.length}`);
    console.log(`  WCAAS TABLES DELETED IN REGISTRY: ${deletedResults.length}`);
    console.log(`  WCAAS TABLES UPDATED IN REGISTRY: ${updateResults.length}`);

    const schemaResults = await Promise.all(schemaToBeUpdated.concat(createdResults).map(async dataset => await http.updateSchema(dataset)));

    console.log(`  WCAAS SCHEMAS UPDATED IN REGISTRY: ${schemaResults.length}`);
}


/**
 * Finds a dataset in the list of datasets
 */
function findMatch(dataset: Dataset, datasetsToCompare: Dataset[]): Dataset {
    return datasetsToCompare.find(other => other.name === dataset.name);
}

/**
 * Checks if the dataset is NOT found in the list of datasets
 */
function doesNotExist(dataset: Dataset, datasetsToCompare: Dataset[]): boolean {
    return !datasetsToCompare.some(other => other.name === dataset.name);
}

/**
 * Prompt user to apply changes
 */
async function promptApproval(): Promise<boolean> {

    const rl = readline.createInterface({
        input: process.stdin, //or fileStream
        output: process.stdout
    });

    process.stdout.write("\nApply changes? ('yes' to proceed): ");

    const it = rl[Symbol.asyncIterator]();
    const response = await it.next();
    rl.close();

    return response.value === 'yes';
}


// TYPES

export type AvroType = 'boolean' | 'bytes' | 'double' | 'float' | 'int' | 'long' | 'string';

export interface Dataset {
    id?: string;
    name: string;
    description: string;
    configuration: {};
    datastore: DatastoreType;
    schema: Schema;
}

export interface Field {
    name: string;
    type: AvroType;
    doc: string;
}

export interface Schema {
    type: 'record';
    name: string;
    namespace: string;
    fields: Field[];
}

