import pulumi
import pulumi_google_native as google
import pulumi_digitalocean as do
import os
from network import network_stack
from k8s import k8s_stack

config = pulumi.Config()
provider = config.require("provider")  # 'gcp' or 'do'
deploy_network = config.get_bool("deploy_network")
deploy_k8s = config.get_bool("deploy_k8s")

# if provider == "gcp" and "GOOGLE_CREDENTIALS" not in os.environ:
#     raise Exception("Missing GOOGLE_CREDENTIALS for GCP")

if provider == "do" and "DIGITALOCEAN_TOKEN" not in os.environ:
    raise Exception("Missing DIGITALOCEAN_TOKEN for DigitalOcean")

if deploy_network:
    network = network_stack(default_region=config.get("default_region") or "us-central1", provider=provider)

if deploy_k8s:
    k8s_cluster = k8s_stack(region=config.get("default_region") or "us-central1",
                            k8s_version=config.get("k8s_version") or "1.20.9-gke.1001",
                            provider=provider)

# Export outputs as needed, for example, the cluster name
if deploy_k8s:
    pulumi.export('cluster_name', k8s_cluster.name)
