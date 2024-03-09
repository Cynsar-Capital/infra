import pulumi
import pulumi_digitalocean as do
import pulumi_mysql as mysql
import pulumi_kubernetes as k8s

def ghost_db_stack(db_cluster_id: str):
    ghost_db = do.DatabaseDb("ghost",
                             cluster_id=db_cluster_id)

    ghost_user = do.DatabaseUser("ghost_user",
                                 cluster_id=db_cluster_id)

    pulumi.export("ghost_db_name", ghost_db.name)
    pulumi.export("ghost_db_user", ghost_user.name)
    pulumi.export("ghost_db_password", ghost_user.password)

    return {
        "name": ghost_db.name,
        "user": ghost_user.name,
        "password": ghost_user.password,
    }

def ghost_stack(cluster_name: str, ghost_db_name: str, ghost_db_user: str, ghost_db_password: str, ghost_db_host: str, ghost_db_port: int):
    app_labels = {"app": "ghost"}

    ghost_deployment = k8s.apps.v1.Deployment(
        "ghost-deployment",
        spec=k8s.apps.v1.DeploymentSpecArgs(
            replicas=1,
            selector=k8s.meta.v1.LabelSelectorArgs(match_labels=app_labels),
            template=k8s.core.v1.PodTemplateSpecArgs(
                metadata=k8s.meta.v1.ObjectMetaArgs(labels=app_labels),
                spec=k8s.core.v1.PodSpecArgs(
                    containers=[
                        k8s.core.v1.ContainerArgs(
                            name="ghost",
                            image="ghost:latest",
                            ports=[k8s.core.v1.ContainerPortArgs(container_port=2368)],
                            env=[
                                k8s.core.v1.EnvVarArgs(name="database__client", value="mysql"),
                                k8s.core.v1.EnvVarArgs(name="database__connection__host", value=ghost_db_host),
                                k8s.core.v1.EnvVarArgs(name="database__connection__user", value=ghost_db_user),
                                k8s.core.v1.EnvVarArgs(name="database__connection__password", value=ghost_db_password),
                                k8s.core.v1.EnvVarArgs(name="database__connection__database", value=ghost_db_name),
                                k8s.core.v1.EnvVarArgs(name="database__connection__port", value=str(ghost_db_port)),
                            ],
                        )
                    ]
                ),
            ),
        ),
    )

    ghost_service = k8s.core.v1.Service(
        "ghost-service",
        metadata=k8s.meta.v1.ObjectMetaArgs(name="ghost"),
        spec=k8s.core.v1.ServiceSpecArgs(
            selector=app_labels,
            ports=[k8s.core.v1.ServicePortArgs(port=80, target_port=2368)],
            type="LoadBalancer",
        ),
    )

    pulumi.export("ghost_service_url", ghost_service.status.load_balancer.ingress[0].ip)
