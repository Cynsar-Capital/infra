import pulumi
import pulumi_google_native.container.v1 as gke
import pulumi_digitalocean as do
import lib.utils as utils
import os

def k8s_stack(region: str, k8s_version: str, provider: str, vpc_id: str = None):
    if provider.lower() == 'gcp':
        # Google Cloud Kubernetes Engine (GKE) Cluster
        cluster = gke.Cluster(
            "gke-cluster",
            location=region,
            initial_node_count=3,  # Updated argument name
            node_config={
                "machine_type": "e2-medium",
            }
        )
        pulumi.export('gke_cluster_name', cluster.name)

    elif provider.lower() == 'do':
        # Validate DigitalOcean Kubernetes versions
        do_k8s_versions = utils.validate_k8s_versions(os.environ.get("DIGITALOCEAN_TOKEN"), k8s_version)
        pulumi.log.info(f"Available k8s versions: {do_k8s_versions}")

        if k8s_version not in do_k8s_versions:
            raise Exception("The specified version is not available in DigitalOcean.")

        # Create a DigitalOcean Kubernetes cluster
        do_cluster = do.KubernetesCluster(
            "do-k8s-cluster",
            region=region,
            version=k8s_version,
            node_pool={
                "name": "default",
                "size": "s-1vcpu-2gb",
                "node_count": 3,
            },
            vpc_uuid=vpc_id
        )
        pulumi.export('do_k8s_cluster_name', do_cluster.name)

    else:
        raise ValueError(f"Unsupported provider: {provider}")

    return cluster if provider.lower() == 'gcp' else do_cluster
