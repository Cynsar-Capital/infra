"""A DigitalOcean Python Pulumi program"""

import pulumi
import pulumi_digitalocean as do
import os
import lib.utils as utils


# Vesions and other global options
default_region = "ams3" # All the infra is on amsterdan
k8s_options = {
    "do": "1.29.1-do.0",
    "k8s": "1.29.1"
}

if "DIGITALOCEAN_TOKEN" not in os.environ:
    raise Exception("Missing DIGITALOCEAN_TOKEN")

# Main VPC
ams_vpc = do.Vpc("ams3-vpc",
                 region=default_region, 
                 ip_range="10.110.0.0/20",
                 name="default-ams3",
                 opts=pulumi.ResourceOptions(
                    import_="e955595a-be66-4f4b-83d5-7c6a75ba2dcf",
                    protect=True
                ))

# K8s Cluster
do_k8s_versions = utils.validate_k8s_versions(os.environ.get("DIGITALOCEAN_TOKEN"), k8s_options["k8s"])

pulumi.log.info("Available k8s versions: {v}".format(v=do_k8s_versions))

if k8s_options["do"] not in do_k8s_versions:
    raise Exception("The version that is available in DO is not the same")

# Create a digital ocean kubernetes cluster
do_k8s_cluster = do.KubernetesCluster("do-k8s-cluster",
    region="ams3",
    version=k8s_options["do"],
    node_pool={
        "name": "default-pool",
        "size": "s-2vcpu-2gb",
        "node_count": 3,
    },
    tags=["pulumi", "k8s-cluster"]
)

# Export the cluster's kubeconfig
pulumi.export('kubeconfig',
    do_k8s_cluster.kube_configs.apply(lambda configs: configs[0]['raw_config']))

# Collect all in a project
prod_project = do.Project(resource_name="production",
                          description="Production environment", 
                          environment="Production",
                          purpose="Production K8S Cluster", 
                          is_default=False,
                          resources=[do_k8s_cluster.cluster_urn])
