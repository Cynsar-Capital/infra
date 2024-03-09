import pulumi
import pulumi_google_native as google
import pulumi_digitalocean as do
import os
from network import network_stack
from k8s import k8s_stack

from ghost import ghost_db_stack, ghost_stack
from database import mysql_db_stack

config = pulumi.Config()
provider = config.require("provider")  # 'gcp' or 'do'
deploy_network = config.get_bool("deploy_network")
deploy_k8s = config.get_bool("deploy_k8s")
deploy_ghost = config.get_bool("deploy_ghost")
deploy_mysql = config.get_bool("deploy_mysql")


if provider == "do" and "DIGITALOCEAN_TOKEN" not in os.environ:
    raise Exception("Missing DIGITALOCEAN_TOKEN for DigitalOcean")

if deploy_network:
    network = network_stack(default_region=config.get("default_region") or "us-central1", provider=provider)

if deploy_k8s:
    k8s_cluster = k8s_stack(region=config.get("default_region") or "us-central1",
                            k8s_version=config.get("k8s_version") or "1.20.9-gke.1001",
                            provider=provider)

if deploy_mysql:
    mysql_db = mysql_db_stack(region=config.get("default_region") or "nyc3",
                              vpc_id=network.id)

if deploy_ghost and deploy_mysql:
    ghost_db = ghost_db_stack(db_cluster_id=mysql_db.id)
    ghost_stack(
        cluster_name=k8s_cluster.name,
        ghost_db_name=ghost_db["name"],
        ghost_db_user=ghost_db["user"],
        ghost_db_password=ghost_db["password"],
        ghost_db_host=mysql_db.private_host,
        ghost_db_port=mysql_db.port,
    )

# Export outputs as needed, for example, the cluster name
if deploy_k8s:
    pulumi.export('cluster_name', k8s_cluster.name)
