import {DatastoreType} from "./registry-http";

const fs = require('fs');

export default function (datastoreType: DatastoreType) {
    return JSON.parse(fs.readFileSync("settings.json"))[datastoreType];
}
