
import pulumi
import pulumi_digitalocean as do
import lib.utils as utils
import os

def k8s_stack(region: str, k8s_version: str, do_version: str, vpc_id: str):
    
    do_k8s_versions = utils.validate_k8s_versions(os.environ.get("DIGITALOCEAN_TOKEN"), k8s_version)

    pulumi.log.info("Available k8s versions: {v}".format(v=do_k8s_versions))

    if do_version not in do_k8s_versions:
        raise Exception("The version that is available in Digital Oceaan is not the same")

# Create a digital ocean kubernetes cluster
    do_k8s_cluster = do.KubernetesCluster("do-k8s-cluster",
        region=region,
        version=do_version,
        node_pool={
            "name": "default-pool",
            "size": "s-2vcpu-2gb",
            "node_count": 3,
        },
        vpc_uuid=vpc_id,
        tags=["pulumi", "k8s-cluster"]
    )

    return do_k8s_cluster
