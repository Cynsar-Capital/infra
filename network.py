# Reparted version for the network stack

import pulumi
import pulumi_digitalocean as do


def network_stack(default_region: str):
    ams_vpc = do.Vpc("ams3-vpc",
                     region=default_region,
                     ip_range="10.110.0.0/20",
                     name="default-ams3",
                     opts=pulumi.ResourceOptions(
                        import_="e955595a-be66-4f4b-83d5-7c6a75ba2dcf",
                        protect=True
                    ))

    return ams_vpc
