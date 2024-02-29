import pulumi
import pulumi_digitalocean as do

def mysql_db_stack( region: str, vpc_id: str):
    do_mysql_db = do.DatabaseCluster("mysql-personal", 
        engine = "mysql", 
        node_count=1,
        version="8",
        region = region,
        size="db-s-1vcpu-1gb",
        private_network_uuid=vpc_id,
        opts = pulumi.ResourceOptions(protect=True),
        tags=["pulumi", "protected"])

    pulumi.export("mysql_db_admin_user", do_mysql_db.user)
    pulumi.export("mysql_db_admin_paswword", do_mysql_db.password)
    pulumi.export("mysql_db_public_host", do_mysql_db.uri)
    pulumi.export("mysql_db_port", do_mysql_db.port)
    pulumi.export("mysql_db_private_host", do_mysql_db.private_uri)

    return do_mysql_db
