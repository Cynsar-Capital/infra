# Cynsar Capital Infrastruture repo

## How to run?

```
python -m venv venv
```

```
source venv/bin/activate
```

```
pip install -r requirements.txt
```

### Setting config

```
pulumi config set provider gcp
pulumi config set default_region us-central1
pulumi config set deploy_network true
pulumi config set deploy_k8s true
```

```
pulumi preview
```

```
pulumi up
```

## Authentication

### Digital Ocean

You need to set your token as such:

```
export DIGITALOCEAN_TOKEN=<token>
```

### Google Cloud

```
gcloud auth login
```

```
gcloud auth application-default login
```
