/**
 * Creates a configuration for Postgres DB Migrations.
 *
 * - Retrieves DB Host and Credentials from AWS SecretManager
 * - Builds a connection string to RDS
 * - Saves connection and rest of config to `yoyo.ini` file in the same directory
 */
const fs = require('fs');
const AWS = require('aws-sdk');
const sm = new AWS.SecretsManager({apiVersion: '2017-10-17', region: 'us-east-2'});

async function retrieveRdsSecret(SecretId) {
    const json = await sm.getSecretValue({SecretId}).promise();
    return JSON.parse(json.SecretString);
}

function createConfig(connectionString) {
    return `
[DEFAULT]

# List of migration source directories. "%(here)s" is expanded to the
# full path of the directory containing this ini file.
sources = %(here)s/postgres

# Verbosity level. Goes from 0 (least verbose) to 3 (most verbose)
verbosity = 3

# Disable interactive features
batch_mode = on

# Database connection string
database = ${connectionString}
`;
}

(async () => {
    const db = await retrieveRdsSecret('rds/wcaasmgmt');
    const config = createConfig(`postgresql://${db.username}:${db.password}@${db.host}`);
    fs.writeFileSync('yoyo.ini', Buffer.from(config));
})();



