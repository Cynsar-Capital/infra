import requests

def validate_k8s_versions(token: str, k8s_version: str) -> str:
    """
    Get the available kubernetes versions for a given region
    https://docs.digitalocean.com/reference/api/api-reference/#operation/kubernetes_list_options

    :param token (str): DigitalOcean API Token
    :param k8s_version (str): The kubernetes version to get the specified DO version slug
    :return (str): The matching DigitalOcean version slug
    :raises Exception if the request gives a non-200 error or if the specified version is not available
    """

    kubernetes_options_url = "https://api.digitalocean.com/v2/kubernetes/options"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(kubernetes_options_url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception("Non 200 response: {code} and {j}".format(
            code=response.status_code,
            j=response.json()
        ))
    else:
        kubernetes_options = response.json()
        versions = kubernetes_options['options']['versions']

        for version in versions:
            if version["slug"].startswith(k8s_version):
                return version["slug"]

        raise Exception(f"The specified version '{k8s_version}' is not available in DigitalOcean.")

def get_my_ip() -> str:
    """
    Get the public IP of the machince running the script

    :return (str): The public IP of the Machine
    """

    response = requests.get(url = "https://ifconfig.me/all.json",
                            headers = { "Content-Type": "application/json"} )

    return response.json()["ip_addr"]
