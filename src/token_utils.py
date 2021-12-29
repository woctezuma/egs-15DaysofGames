import base64

import requests
from requests.auth import HTTPBasicAuth


def get_egs_hosts() -> dict[str, str]:
    # Reference: https://github.com/derrod/legendary/blob/master/legendary/api/egs.py
    egs_hosts = dict(
        _oauth_host="account-public-service-prod.ol.epicgames.com",
        _launcher_host="launcher-public-service-prod.ol.epicgames.com",
        _entitlements_host="entitlement-public-service-prod.ol.epicgames.com",
        _catalog_host="catalog-public-service-prod.ol.epicgames.com",
        _ecommerce_host="ecommerceintegration-public-service-ecomprod.ol.epicgames.com",
        _datastorage_host="datastorage-public-service-liveegs.live.use1a.on.epicgames.com",
        _library_host="library-service.live.use1a.on.epicgames.com",
        _store_gql_host="store-launcher.epicgames.com",
        _artifact_service_host="artifact-public-service-prod.beee.live.use1a.on.epicgames.com",
    )

    return egs_hosts


def get_egs_oauth_url() -> str:
    egs_hosts = get_egs_hosts()
    _oauth_host = egs_hosts["_oauth_host"]

    url = f"https://{_oauth_host}/account/api/oauth/token"

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
    client_id: str,
    client_secret: str,
    body_data: dict,
    rely_on_oauth_basic: bool = False,
    verbose: bool = True,
) -> str | None:
    if rely_on_oauth_basic:
        r = requests.post(
            url=get_egs_oauth_url(),
            data=body_data,
            auth=HTTPBasicAuth(client_id, client_secret),
        )
    else:
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
    client_id: str,
    client_secret: str,
    rely_on_oauth_basic: bool = False,
    ask_for_long_token: bool = False,
    verbose: bool = True,
) -> str | None:
    # Reference: https://github.com/MixV2/EpicResearch/blob/master/docs/auth/grant_types/client_credentials.md
    body_data = {"grant_type": "client_credentials"}
    if ask_for_long_token:
        body_data["token_type"] = "eg1"
    access_token = get_access_token(
        client_id, client_secret, body_data, rely_on_oauth_basic, verbose
    )
    return access_token


def get_access_token_with_authorization_code(
    client_id: str,
    client_secret: str,
    authorization_code: str,
    rely_on_oauth_basic: bool = False,
    ask_for_long_token: bool = False,
    verbose: bool = True,
) -> str | None:
    # Reference: https://github.com/MixV2/EpicResearch/blob/master/docs/auth/grant_types/authorization_code.md
    body_data = {"grant_type": "authorization_code", "code": f"{authorization_code}"}
    if ask_for_long_token:
        body_data["token_type"] = "eg1"
    access_token = get_access_token(
        client_id, client_secret, body_data, rely_on_oauth_basic, verbose
    )
    return access_token


def get_oauth_headers(access_token: str) -> dict[str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    return headers
