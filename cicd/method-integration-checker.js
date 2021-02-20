/**
 * Script to find Resource Methods that are missing integrations.
 *
 * Gives more detail on the following error when running a terraform apply:
 *  Error creating API Gateway Deployment: BadRequestException: No integration defined for method
 */

const yargs = require('yargs');
const AWS = require('aws-sdk');

const argv = yargs
    .option('region', {
        description: 'AWS Region',
        type: 'string',
        required: true
    })
    .option('rest-api-name', {
        description: 'Name of the rest API',
        type: 'string',
        default: 'cyberscan-api-root'
    }).argv;

AWS.config.update({region: argv.region});

const ag = new AWS.APIGateway({apiVersion: '2015-07-09'});

(async () => {
    const restApiId = await findRestApiIdByName(argv.restApiName);
    const resources = await ag.getResources({restApiId}).promise();

    console.log("Missing Integrations:");
    const methodConfigs = resources.items.flatMap(i =>
        Object.keys(i.resourceMethods || {})
            .map(async httpMethod => {

                const params = {
                    httpMethod,
                    resourceId: i.id,
                    restApiId
                };

                const method = await ag.getMethod(params).promise();

                // log any missing integrations
                if (!method.methodIntegration) {
                    console.log(`${httpMethod} ${i.path}.`);
                }
            }));

})();

async function findRestApiIdByName(restApiName) {
    const apis = await ag.getRestApis().promise();
    return apis.items.filter(i => i.name === restApiName)[0].id;
}


