#!/usr/bin/env node
const fs = require('fs');
const faker = require('faker');
const dateFormat = require('dateformat');
const axios = require('axios');
const yargs = require('yargs');
const path = require("path");

const argv = yargs
    .option('keyspaces', {
        alias: 'k',
        description: 'Keyspaces to use',
        type: 'array',
        default: ['scan_mgmt']
    })
    .option('rows', {
        alias: 'r',
        description: 'Rows to generate',
        type: 'number',
        default: 5
    })
    .option('host', {
        alias: 'h',
        description: 'API host',
        type: 'string',
        default: 'http://a597bff62752011eab4cf0a5d4ecb7a7-1667787124.us-east-1.elb.amazonaws.com:8080'
    })
    .option('cluster', {
        alias: 'c',
        description: 'Cluster ID',
        type: 'number',
        default: 1003
    })
    .option('account', {
        alias: 'a',
        description: 'Customer account ID',
        type: 'string',
        default: 'dantenant'
    })
    .option('user', {
        alias: 'u',
        description: 'User ID',
        type: 'string',
        default: '123'
    })
    .argv;

const KEYSPACES = argv.keyspaces;
const ROW_COUNT = argv.rows;
const HOST = argv.host;
const CLUSTER_ID = argv.cluster;
const AXIOS_OPTIONS = {
    headers: {
        'X-netscan-CustomerAccountId': argv.account,
        'X-netscan-UserId': argv.user
    }
};

// Get random value based on column name/type
var getRandomValue = function (name, type) {
    if (name.includes('ID')) {
        return faker.random.uuid();
    }
    if (name.includes('EMAIL')) {
        return faker.internet.email();
    }
    if (name.includes('IP')) {
        return faker.internet.ip();
    }
    if (name.includes('SERVERS')) {
        return faker.internet.domainName();
    }
    if (name.includes('PORT')) {
        return faker.random.number(65535);
    }
    if (name.includes('PORT')) {
        return faker.random.number(65535);
    }
    if (name.includes('DUNS')) {
        return faker.helpers.replaceSymbolWithNumber("#########");
    }
    if (type === 'timestamp') {
        return dateFormat(faker.date.future(), 'isoDateTime');
    }
    if (type === 'int') {
        return faker.random.number().toString();
    }
    return faker.random.words();
}

// Keep random values for same row and column name
let valueByRowAndName = Array.apply(null, Array(ROW_COUNT)).map(function () {
    return {};
});

KEYSPACES.forEach(keyspace => {
    fs.readdir(path.resolve(__dirname, `../config/${keyspace}`), function (err, jsons) {
        jsons.forEach(json => {
            let table = JSON.parse(fs.readFileSync(path.resolve(__dirname, `../config/${keyspace}/${json}`)));

            // Get columns definition
            let columns = [];
            table['columnDefinitions'].forEach(column => {
                let columnDef = column.split(' ');
                columns.push({
                    name: columnDef[0],
                    type: columnDef[1]
                });
            });

            for (var i = 0; i < ROW_COUNT; ++i) {
                let record = {
                    jsonClause: {},
                    ttl: 31556952
                };

                // Add random value for each column
                columns.forEach(column => {
                    if (!valueByRowAndName[i][column.name]) {
                        valueByRowAndName[i][column.name] = getRandomValue(column.name, column.type);
                    }
                    record['jsonClause'][column.name] = valueByRowAndName[i][column.name];
                });

                // REST call to insert a row
                axios
                    .post(`${HOST}/api/clusters/${CLUSTER_ID}/keyspaces/${keyspace}/tables/${table.name}/insert`, record, AXIOS_OPTIONS)
                    .then(res => {
                        console.log(`statusCode: ${res.status}`);
                    })
                    .catch(error => {
                        console.log('RECORD', record);
                        console.error(error.response.data);
                    });
            }
        });
    });
});
