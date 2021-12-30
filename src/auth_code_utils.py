import requests

from src.io_utils import load_epic_cookie_from_disk, get_epic_cookie_file_name


def get_egs_auth_url() -> str:
    url = "https://www.epicgames.com/id/api/redirect"
    return url


def get_auth_client() -> dict[str, str | None]:
    # Reference: https://github.com/MixV2/EpicResearch/blob/master/docs/auth/auth_clients.md
    auth_client = {
        "name": "graphqlWebsite",
        "id": "319e1527d0be4457a1067829fc0ad86e",
        "secret": None,
    }

    return auth_client


def get_url_to_visit_for_auth_code(client_id: str = None, verbose: bool = True) -> str:
    url = get_egs_auth_url()

    if client_id is None:
        client = get_auth_client()
        client_id = client["id"]

    full_url = f"{url}?clientId={client_id}&responseType=code"

    if verbose:
        print(f"Please visit {full_url} in a web-browser to find `authorizationCode`.")

    return full_url


def get_authorization_code(
    client_id: str = None, cookie_fname: str = None, verbose: bool = True
) -> str:
    full_url = get_url_to_visit_for_auth_code(client_id=client_id, verbose=verbose)
    cookies = load_epic_cookie_from_disk(fname=cookie_fname)

    if len(cookies) > 0:
        r = requests.get(url=full_url, cookies=cookies)
    else:
        r = requests.get(url=full_url)
    r.raise_for_status()

    data = r.json()

    try:
        code = data["authorizationCode"]
        if code is None:
            code = ""
    except KeyError:
        code = ""

    if verbose:
        print(f"Authorization code: {code} (automatically retrieved)")

    return code


if __name__ == "__main__":
    cookie_name = "../" + get_epic_cookie_file_name()
    authorization_code = get_authorization_code(cookie_fname=cookie_name, verbose=True)
