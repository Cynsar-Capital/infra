"""A DigitalOcean Python Pulumi program"""

from k8s import k8s_stack
import pulumi
import pulumi_digitalocean as do
import os
import lib.utils as utils

from network import network_stack

# Vesions and other global options
default_region = "ams3" # All the infra is on amsterdan
k8s_options = {
    "do": "1.29.1-do.0",
    "k8s": "1.29.1"
}

if "DIGITALOCEAN_TOKEN" not in os.environ:
    raise Exception("Missing DIGITALOCEAN_TOKEN")

# Network
ams_vpc = network_stack(default_region)

# K8s Cluster
do_k8s_cluster = k8s_stack(region = default_region,
                           k8s_version = k8s_options["k8s"],
                           do_version = k8s_options["do"],
                           vpc_id= ams_vpc.id)

# Export the cluster's kubeconfig
pulumi.export('kubeconfig',
    do_k8s_cluster.kube_configs.apply(lambda configs: configs[0]['raw_config']))

do_mysql_db = do.DatabaseCluster("mysql-personal", 
    engine = "mysql", 
    node_count=1,
    version="8",
    region = default_region,
    size="db-s-1vcpu-1gb",
    private_network_uuid=ams_vpc.id,
    opts = pulumi.ResourceOptions(protect=True),
    tags=["pulumi", "protected"])

# Collect all in a project
prod_project = do.Project(resource_name="production",
    description="Production environment", 
    environment="Production",
    purpose="Production K8S Cluster", 
    is_default=False,
    resources=[do_k8s_cluster.cluster_urn,
               do_mysql_db.cluster_urn])

