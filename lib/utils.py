import requests

def validate_k8s_versions(token: str, k8s_version: str) -> list[str]:
    """
    Get the available kubernetes versions for a given region
    https://docs.digitalocean.com/reference/api/api-reference/#operation/kubernetes_list_options

    :param token (str): DigitalOcean API Token
    :param k8s_version (str): The kubernetes version to get the specified DO version slug
    :return (list[str]): A list of available kubernetes versions
    :raises Excpection if the request gives a non 200 error
    """

    kubernetes_options_url = "https://api.digitalocean.com/v2/kubernetes/options"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(kubernetes_options_url, headers=headers)


    # Check if the request was successful
    if response.status_code != 200:
        raise Exception("Non 200 response: {resp}".format(resp=response))
    else:
        kubernetes_options = response.json()
        versions = kubernetes_options['options']['versions']
        
        do_versions = []

        for version in versions:
            if version["kubernetes_version"] == k8s_version:
                do_versions.append(version["slug"])

        return do_versions
