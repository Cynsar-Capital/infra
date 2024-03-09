import pulumi
import pulumi_google_native.compute.v1 as gcp_compute
import pulumi_digitalocean as do

def network_stack(default_region: str, provider: str):
    if provider.lower() == 'gcp':
        # Google Cloud VPC Network
        gcp_vpc = gcp_compute.Network(
            "gcp-vpc",
            auto_create_subnetworks=True,  # Automatically create subnetworks in each region
            description="A VPC network for GCP resources"
        )
        pulumi.export('gcp_vpc_name', gcp_vpc.name)

    elif provider.lower() == 'do':
        # DigitalOcean VPC
        do_vpc = do.Vpc(
            "do-vpc",
            region=default_region,
            name="default-vpc",
            opts=pulumi.ResourceOptions(
                protect=True  # Protect the resource from accidental deletion
            )
        )
        pulumi.export('do_vpc_name', do_vpc.name)
        pulumi.export('do_vpc_id', do_vpc.id)

    else:
        raise ValueError(f"Unsupported provider: {provider}")

    return gcp_vpc if provider.lower() == 'gcp' else do_vpc
