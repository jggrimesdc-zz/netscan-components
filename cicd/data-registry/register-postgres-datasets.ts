import {AvroType, Dataset, Field, registerDatasets} from "./register-datasets";
import getSettings from "./settings";

const yargs = require('yargs');
const {Client} = require('pg');
const AWS = require('aws-sdk');
const sm = new AWS.SecretsManager({apiVersion: '2017-10-17', region: 'us-east-2'});
const {schemas, rdsSecretKey} = getSettings("postgres");

const argv = yargs
    .option('auto-approve', {
        description: 'Automatically execute changes without prompting.',
        type: 'boolean',
        default: false
    }).argv;

let client;

(async () => {
    try {
        const db = await retrieveRdsSecret(rdsSecretKey);
        client = await newClient(db);
        await client.connect();
        const datasets = await getDatasets(db);
        await registerDatasets(datasets, 'postgres', argv);
    } finally {
        if (client) {
            await client.end();
        }
    }
})();

async function getDatasets(db: DatabaseSecret): Promise<Dataset[]> {
    const tables = await Promise.all(schemas.map(schema => getTables(schema)));

    return await Promise.all(tables.flat()
        .map(async (table: PostgresTable): Promise<Dataset> => ({
            name: `${table.schemaName}.${table.tableName}`.slice(0, 48),
            description: table.comment || 'Missing',
            configuration: getConfiguration(table, db),
            datastore: 'postgres',
            schema: {
                type: 'record',
                name: table.tableName,
                namespace: `com.netscan.scan.postgres.${table.schemaName}`,
                fields: await getFields(table)
            }
        })));
}


function getConfiguration(table: PostgresTable, db: DatabaseSecret): PostgresConfiguration {
    return {
        url: db.host,
        port: db.port,
        username: db.username,
        password: db.password,
        db: table.schemaName,
        table: table.tableName
    };
}


async function getTables(schemaName: string): Promise<PostgresTable[]> {
    const result = await client.query(`
    SELECT t.table_name, obj_description(pgc.oid, 'pg_class') as comment
    FROM information_schema.tables t JOIN 
         pg_catalog.pg_class pgc ON t.table_name = pgc.relname 
    WHERE t.table_schema='${schemaName}'`);

    return result.rows.map((row): PostgresTable => ({
        schemaName,
        tableName: row.table_name,
        comment: row.comment
    }));
}


async function getFields(table: PostgresTable): Promise<Field[]> {
    const result = await client.query(`
   SELECT c.column_name, c.data_type, col_description(pgc.oid, c.ordinal_position) as comment
    FROM information_schema.columns c JOIN 
         pg_catalog.pg_class pgc ON c.table_name = pgc.relname 
    WHERE table_schema = '${table.schemaName}' 
      AND table_name = '${table.tableName}'`);

    return result.rows.map((row): Field => {

        const dataType = row.data_type.toLowerCase().split(' ')[0];
        const type = POSTGRES_TO_AVRO_MAPPINGS[dataType];

        if (!type) {
            throw new Error(`Avro data type mapping not found. Schema: ${table.schemaName}, Table: ${table.tableName}, Column: ${row.column_name}, Type: ${row.data_type}`);
        }

        return {
            name: row.column_name,
            type,
            doc: row.comment || ""
        };
    });
}

async function retrieveRdsSecret(SecretId: string): Promise<any> {
    const json = await sm.getSecretValue({SecretId}).promise();
    return JSON.parse(json.SecretString);
}

async function newClient(db: DatabaseSecret): Promise<typeof Client> {
    return new Client({
        host: db.host,
        port: db.port,
        user: db.username,
        password: db.password
    });
}

// TYPES

const POSTGRES_TO_AVRO_MAPPINGS: { [key: string]: AvroType } =
    Object.freeze({
        array: "string",
        boolean: "boolean",
        character: "string",
        double: "double",
        integer: "int",
        text: "string",
        timestamp: "long",
        tsvector: "string"
    });

interface PostgresTable {
    schemaName: string;
    tableName: string;
    comment: string;
}

interface PostgresConfiguration {
    url: string;
    port: number;
    db: string;
    username: string;
    password: string;
    table: string;
}

interface DatabaseSecret {
    username: string;
    password: string;
    engine: string;
    host: string;
    port: number;
    dbInstanceIdentifier: string;
}
