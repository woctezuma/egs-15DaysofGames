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


if __name__ == "__main__":
    _ = get_url_to_visit_for_auth_code(verbose=True)
