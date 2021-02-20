const k8s = require('@kubernetes/client-node');
const kc = new k8s.KubeConfig();
kc.loadFromDefault();
const k8sApi = kc.makeApiClient(k8s.CoreV1Api);

export default async (): Promise<string[]> => {
    const res = await k8sApi.listNamespacedPod('wcaas-crud');
    const pods = res.body.items.filter(item => item.metadata.labels.app === 'cassandracluster');
    return pods.map(pod => pod.status.podIP);
}

