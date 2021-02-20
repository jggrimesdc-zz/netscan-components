/**
 * Compiles an OpenApi documentation.
 *
 * Steps:
 * 1. Retrieves the base documentation from API Gateway in a JSON format
 * 2. Iterates through the src/scan/lambdas for JSON files that match "**_handler.json"
 * 3. Validates each individual JSON files to conform to OpenApi 3.0
 * 4. Merges document path to base documentation
 * 5. Saves a copy locally, optionally can push to S3 as well.
 *
 * Arguments:
 * -t or --test                runs validation mode only.  won't compile documents.  all other arguments are ignored.
 * --aws_region                apigateway's region (for retrieving the base documentation)
 * --rest_api_id               apigateway's rest api id (for retrieving the base documentation)
 * --api_deploy_stage_name     apigateway's stage name (for retrieving the base documentation)
 * --s3_documentation_path     the s3 save location to put the final documentation (bucket + key prefix all in one string)
 */

// cwd to the path of the script
process.chdir(process.mainModule.path + '/../cicd')

const AWS = require('aws-sdk'),
    validator = require('oas-validator'),
    glob = require("glob"),
    fs = require("fs");

const args = process.argv.slice(2);

// for convenience, running this script w/o args will use the sandbox config
const DEFAULT_SANDBOX_CONFIG = {
    region: 'us-east-1',
    restApiId: 'c1tydbup25',
    stageName: 'sandbox',
    s3DocumentationPath: ''
};

// maps arguments to runtime config
// ex. "--aws_region=us-east-1" will set the "config.region" variable to "us-east-1"
const ARGUMENT_MAP = {
    'aws_region': 'region',
    'rest_api_id': 'restApiId',
    'api_deploy_stage_name': 'stageName',
    's3_documentation_path': 's3DocumentationPath',
}

const config = {
    ...DEFAULT_SANDBOX_CONFIG
};

// sets config
args.forEach(arg => {
    if (arg.startsWith('--')) {
        const keyValue = arg.replace(/^--/, '').split('=');
        const mapping = ARGUMENT_MAP[keyValue[0]];

        if (mapping) {
            config[mapping] = keyValue[1];
        }
    }
});

console.log('Using config:\n' + JSON.stringify(config, null, 2));

AWS.config.update({region: config.region});

const ag = new AWS.APIGateway({apiVersion: '2015-07-09'});
const BASE_PATH = "../src/scan/lambdas";
const OUTPUT_PATH = `../cyberscan-api-${config.stageName}-${config.restApiId}.json`;
const LAMBDA_DOCS_PATH = `${BASE_PATH}/**/*.json`;

/**
 * Script Main
 *
 * Compiles an OpenApi 3.0 document:
 * - Retrieves a base document from AWS
 * - Merge individual documentation for each lambda into the base document
 * - Lints the compiled document to make sure it conforms to the spec
 * - Writes final JSON file somewhere
 */
(async () => {
    if (args.indexOf('--test') > -1 || args.indexOf('-t') > -1) {
        await validateDocumentParts();
    } else {
        const documentation = await compileDocumentation();

        if (config.s3DocumentationPath) {
            await saveDocumentationToS3(documentation);
        }
    }
})();


/**
 * Pushes the documentation to the specified S3 bucket (in the config)
 */
async function saveDocumentationToS3(documentation) {

    const base64data = Buffer.from(JSON.stringify(documentation, null, 2), 'binary');
    const s3PathParts = config.s3DocumentationPath.split('/').filter(x => !!x);
    const bucket = s3PathParts.shift();
    const keyPrefix = s3PathParts.join('/');
    const fileName = OUTPUT_PATH.split('/').pop();

    const params = {
        Body: base64data,
        Bucket: bucket,
        Key: `${keyPrefix}/${fileName}`
    };

    await new AWS.S3().putObject(params).promise();

    console.log(`Saved file to S3: s3://${params.Bucket}/${params.Key}`);
}


/**
 * Retrieves the base documentation from AWS Api Gateway
 *
 * @param restApiId api gateway rest api id
 * @param stageName api gateway stage
 * @returns {Promise < any >}
 */
async function getApiGatewayExport({restApiId, stageName}) {

    const params = {
        restApiId: config.restApiId,
        stageName: config.stageName,
        exportType: 'OAS30',
        accepts: 'application/json',
    };

    // retrieve
    const response = await ag.getExport(params).promise();
    return JSON.parse(response.body);
}

/**
 * Validates that local documentation conforms to the OpenApi 3.0 spec
 */
async function validateDocumentParts() {

    const lambdaDocs = await findLambdaDocumentation();

    for (const filename of lambdaDocs) {
        let lambdaDoc = JSON.parse(fs.readFileSync(filename));
        console.log(filename);
        await validateSchema(lambdaDoc, filename);
    }

    console.log(`Validated ${lambdaDocs.length} document(s).`);
}

/**
 * @param documentation - base documentation pulled from AWS ApiGateway
 */
async function compileDocumentation() {

    const documentation = await getApiGatewayExport(config);

    documentation.info.version = new Date().toISOString();

    const lambdaDocs = await findLambdaDocumentation();

    // merge individual documents to the base document
    for (const filename of lambdaDocs) {
        let lambdaDoc = JSON.parse(fs.readFileSync(filename));
        await validateSchema(lambdaDoc, filename); // validate individual files before merging

        // merge (instead of overwrite)
        documentation.paths = mergeDeep(documentation.paths, lambdaDoc.paths);

        // overwrite (instead of merge)
        // Object.keys(lambdaDoc.paths)
        //   .forEach(key => documentation.paths[key] = lambdaDoc.paths[key]);
    }

    // validate the newly merged document
    await validateSchema(documentation);

    fs.writeFileSync(OUTPUT_PATH, JSON.stringify(documentation, null, 2));

    console.log(`Merged and validated ${lambdaDocs.length} document(s).`);
    console.log(`Documentation compiled successfully.`);
    console.log(`Saved copy locally: ${OUTPUT_PATH}`);

    return documentation;
}

/**
 * Validates an OpenApi schema
 *
 * @param schema a JSON object that represents an OpenApi schema
 * @param filename the document filename for reporting errors back
 * @returns {Promise < unknown >}
 */
async function validateSchema(schema, filename) {
    return new Promise(resolve => {
        validator.validate(schema, {}, (result) => {

            if (result) {
                const {options} = result;
                if (!options.valid) {
                    const messages = [
                        `Document failed OAS30 validation.`,
                        `Message   = ${result.message}`,
                        `Json Path = ${options.context.pop()}`,
                        `File      = ${filename || OUTPUT_PATH}`
                    ];
                    throw new Error(messages.join('\n'));
                }
            }

            resolve(result ? result.options : true);
        });
    });
}

/**
 * Returns are list of paths to each lambda document
 */
async function findLambdaDocumentation() {
    return new Promise(resolve => {
        glob(LAMBDA_DOCS_PATH, (er, files) => resolve(files));
    });
}

/**
 * Performs a deep merge of objects and returns new object. Does not modify
 * objects (immutable) and merges arrays via concatenation.
 *
 * @param {...object} objects - Objects to merge
 * @returns {object} New object with merged key/values
 */
function mergeDeep(...objects) {
    const isObject = obj => obj && typeof obj === 'object';

    return objects.reduce((prev, obj) => {
        Object.keys(obj).forEach(key => {
            const pVal = prev[key];
            const oVal = obj[key];

            // TODO -- security is contradicting itself between AWS/TF and the OpenApi spec that says Array should be empty...
            if (key === 'security') {
                delete prev[key];
                delete obj[key];
                return;
            }

            if (Array.isArray(pVal) && Array.isArray(oVal)) {
                prev[key] = pVal.concat(...oVal).filter((v, i, a) => a.indexOf(v) === i); // unique values only
            } else if (isObject(pVal) && isObject(oVal)) {
                prev[key] = mergeDeep(pVal, oVal);
            } else {
                prev[key] = oVal;
            }
        });

        return prev;
    }, {});
}
