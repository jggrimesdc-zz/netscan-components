import {Dataset, Schema} from "./register-datasets";

const axios = require('axios');

const TAG = 'scan';
const REGISTRY_URL = 'http://registry-service.qos:10143/api/v1';

export type DatastoreType = 'postgres' | 'wcaas';

async function getDatasets(datastore: DatastoreType): Promise<Dataset[]> {
    const response = await axios.get(`${REGISTRY_URL}/asset/dataset?tags=${TAG}`);
    const responseBody = await response.data;
    return responseBody.results.filter(dataset => dataset.datastore === datastore);
}

async function createDataset(dataset: Dataset): Promise<Dataset> {

    const payload = {
        name: dataset.name,
        description: dataset.description,
        configuration: dataset.configuration,
        datastore: dataset.datastore
    };

    const response = await axios.post(`${REGISTRY_URL}/asset/dataset`, payload);
    const responseBody = await response.data;
    await axios.post(`${REGISTRY_URL}/asset/dataset/${responseBody.id}/tag`, {tags: [TAG]});
    return {
        id: responseBody.id,
        ...dataset
    };
}

async function updateDataset({id, name, description}: Dataset): Promise<void> {
    await axios.put(`${REGISTRY_URL}/asset/dataset/${id}`, {name, description});
}

async function deleteDataset({id}: Dataset): Promise<void> {
    await axios.delete(`${REGISTRY_URL}/asset/dataset/${id}`);
}

async function getSchema({id}: Dataset): Promise<Partial<Schema>> {
    try {
        const response = await axios.get(`${REGISTRY_URL}/asset/dataset/${id}/schema`);
        const responseBody = await response.data;
        return responseBody.schema;
    } catch (e) {
        if (e.response.status === 404) {
            return {};
        } else {
            throw e;
        }
    }
}

async function updateSchema({id, schema}: Dataset): Promise<void> {
    await axios.post(`${REGISTRY_URL}/asset/dataset/${id}/schema`, {level: "none"});
    await axios.post(`${REGISTRY_URL}/asset/dataset/${id}/schema`, {schema});
}

export default {
    getDatasets,
    createDataset,
    updateDataset,
    deleteDataset,
    getSchema,
    updateSchema
};
