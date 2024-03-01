import pulumi
import pulumi_digitalocean as do
import pulumi_mysql as mysql

def ghost_db_stack(db_cluster_id: str):
    ghost_db = do.DatabaseDb("ghost", 
                             cluster_id=db_cluster_id)

    # We might need to provide grants to the user
    ghost_user = do.DatabaseUser("ghost_user",
                                 cluster_id=db_cluster_id)

    pulumi.export("ghost_db_name", ghost_db.name)
    pulumi.export("ghost_db_user", ghost_user.name)
    pulumi.export("ghost_db_password", ghost_user.password)


