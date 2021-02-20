const k8s = require('@kubernetes/client-node');
const kc = new k8s.KubeConfig();
kc.loadFromDefault();
const k8sApi = kc.makeApiClient(k8s.CoreV1Api);
const yargs = require('yargs');

const argv = yargs
    .option('max', {
        alias: 'm',
        description: 'Max IPs to return',
        type: 'number',
    }).argv;

(async () => {
    const res = await k8sApi.listNamespacedPod('wcaas-crud');
    const pods = res.body.items.filter(item => item.metadata.labels.app === 'cassandracluster');
    const ips = pods.map(pod => pod.status.podIP);

    if (argv.max) {
        console.log(ips.slice(0, argv.max).join(','));
    } else {
        console.log(ips.join(','));
    }
})();

