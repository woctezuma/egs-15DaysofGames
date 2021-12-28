import base64

import requests


def get_egs_oauth_url() -> str:
    url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    return url


def encode_in_base64(s: str) -> str:
    # Reference: https://stackoverflow.com/a/41437531/376454
    base64_str = base64.b64encode(s.encode()).decode()
    return base64_str


def convert_to_base64_secret(client_id: str, client_secret: str) -> str:
    s = f"{client_id}:{client_secret}"
    base64_secret = encode_in_base64(s)
    return base64_secret


def get_secret_headers(client_id: str, client_secret: str) -> dict:
    secret = convert_to_base64_secret(client_id, client_secret)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"basic {secret}",
    }
    return headers


def get_access_token(
    client_id: str, client_secret: str, body_data: dict, verbose: bool = True
) -> str | None:
    r = requests.post(
        url=get_egs_oauth_url(),
        data=body_data,
        headers=get_secret_headers(client_id, client_secret),
    )

    if r.ok:
        data = r.json()
        access_token = data["access_token"]

        if verbose:
            print(data)
    else:
        access_token = None

        if verbose:
            print(r.status_code)

    return access_token


def get_access_token_with_client_credentials(
    client_id: str, client_secret: str, verbose: bool = True
) -> str | None:
    # Reference: https://github.com/MixV2/EpicResearch/blob/master/docs/auth/grant_types/client_credentials.md
    body_data = {"grant_type": "client_credentials"}
    access_token = get_access_token(client_id, client_secret, body_data, verbose)
    return access_token


def get_access_token_with_authorization_code(
    client_id: str, client_secret: str, authorization_code: str, verbose: bool = True
) -> str | None:
    # Reference: https://github.com/MixV2/EpicResearch/blob/master/docs/auth/grant_types/authorization_code.md
    body_data = {"grant_type": "authorization_code", "code": f"{authorization_code}"}
    access_token = get_access_token(client_id, client_secret, body_data, verbose)
    return access_token


def get_oauth_headers(access_token: str) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    return headers
