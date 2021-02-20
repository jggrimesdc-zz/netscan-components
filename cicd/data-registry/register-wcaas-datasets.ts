import getPodIps from './cassandra-pod-ips';
import {AvroType, Dataset, Field, registerDatasets} from './register-datasets';
import getSettings from "./settings";
import {DatastoreType} from "./registry-http";

const yargs = require('yargs');
const sigV4 = require('aws-sigv4-auth-cassandra-plugin');
const cassandra = require('cassandra-driver');
const fs = require('fs');

// config
const datastoreType: DatastoreType = "wcaas";
const {region, datacenter} = getSettings(datastoreType);

const argv = yargs
    .option('environment', {
        alias: 'e',
        description: 'Environment (ex. dev, qa)',
        type: 'string',
        require: true
    })
    .option('auto-approve', {
        description: 'Automatically execute changes without prompting.',
        type: 'boolean',
        default: false
    }).argv;

const TF_CONFIG = JSON.parse(fs.readFileSync(`../../terraform/config/${argv.environment.toLowerCase()}.terraform.tfvars.json`));

let client;
(async () => {
    try {
        client = await newClient();
        const datasets = await getDatasets();
        await registerDatasets(datasets, datastoreType, argv);
    } finally {
        if (client) {
            client.shutdown(); // must shutdown or the script will hang indefinitely
        }
    }
})();

async function getDatasets(): Promise<Dataset[]> {

    // find all keyspaces
    const keyspaces = await getKeyspaces();

    // find tables in each keyspace
    const tables = await Promise.all(keyspaces.map(keyspace => getTables(keyspace)));

    // find columns for each table, and map to a Dataset object
    return await Promise.all(tables.flat().map(async (table: CassandraTable): Promise<Dataset> => ({
        name: `${table.keyspaceName}.${table.tableName}`.slice(0, 48),
        description: table.comment || 'Missing',
        configuration: getConfiguration(table),
        datastore: datastoreType,
        schema: {
            type: 'record',
            name: table.tableName,
            namespace: `com.netscan.scan.wcaas.${table.keyspaceName}`,
            fields: await getFields(table)
        },
    })));
}

function getConfiguration(table: CassandraTable): WcaasConfiguration {
    return {
        clusterId: TF_CONFIG['wc_cluster_id'],
        keyspace: table.keyspaceName,
        table: table.tableName
    };
}

async function getKeyspaces(): Promise<string[]> {
    const result = await client.execute("SELECT * FROM system_schema.keyspaces");
    return result.rows
        .map(row => row['keyspace_name'])
        .filter(keyspace => !keyspace.startsWith("system")); // omit system keyspaces
}

async function getTables(keyspaceName: string): Promise<CassandraTable[]> {
    const result = await client.execute(`SELECT * FROM system_schema.tables WHERE keyspace_name = '${keyspaceName}'`);
    return result.rows
        .filter(row => row.table_name !== 'database_migrations') // leave out
        .map((row): CassandraTable => ({
            keyspaceName: row.keyspace_name,
            tableName: row.table_name,
            comment: row.comment
        }));
}

async function getFields(table: CassandraTable): Promise<Field[]> {
    const result = await client.execute(`SELECT * FROM system_schema.columns WHERE keyspace_name = '${table.keyspaceName}' AND table_name = '${table.tableName}'`);
    return result.rows.map((row): Field => ({
        name: row.column_name,
        type: CASSANDRA_TO_AVRO_MAPPINGS[row.type],
        doc: row.kind === 'partition_key' ? 'Partition Key' : '' // TODO get column comment
    }));
}

async function newClient() {

    const contactPoints = await getPodIps();
    const authProvider = new sigV4.SigV4AuthProvider({
        region,
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
    });

    return new cassandra.Client({
        contactPoints,
        authProvider,
        localDataCenter: datacenter
    });
}

// TYPES

const CASSANDRA_TO_AVRO_MAPPINGS: { [key: string]: AvroType } =
    Object.freeze({
        ascii: "string",
        bigint: "long",
        blob: "bytes",
        boolean: "boolean",
        counter: "long",
        date: "string",
        decimal: "double",
        double: "double",
        float: "float",
        inet: "string",
        int: "int",
        smallint: "int",
        text: "string",
        time: "string",
        timestamp: "string",
        timeuuid: "string",
        tinyint: "boolean",
        uuid: "string",
        varchar: "string",
        varint: "int"
    });

interface CassandraTable {
    keyspaceName: string;
    tableName: string;
    comment: string;
}

export interface WcaasConfiguration {
    clusterId: string;
    keyspace: string;
    table: string;
}
