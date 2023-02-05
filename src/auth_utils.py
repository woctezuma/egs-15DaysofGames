import requests

from src.auth_code_utils import get_authorization_code, get_url_to_visit_for_auth_code
from src.auth_token_utils import (
    get_access_token_with_authorization_code,
    get_access_token_with_client_credentials,
    get_oauth_headers,
)
from src.download_utils import get_egs_url
from src.io_utils import (
    get_auth_client_filename,
    get_epic_cookie_file_name,
    load_target_auth_client,
)


def get_token(
    client: dict[str, str | None],
    authorization_code: str = "",
    rely_on_oauth_basic: bool = False,
    ask_for_long_token: bool = False,
    verbose: bool = True,
) -> str | None:
    if client["secret"] is None:
        if verbose:
            print("No access token, because the client secret is unknown.")
        access_token = None
    else:
        if len(authorization_code) == 0:
            if verbose:
                print("Using client credentials.")
            access_token = get_access_token_with_client_credentials(
                client["id"],
                client["secret"],
                rely_on_oauth_basic=rely_on_oauth_basic,
                ask_for_long_token=ask_for_long_token,
                verbose=verbose,
            )
        else:
            if verbose:
                print("Using authorization code.")
            access_token = get_access_token_with_authorization_code(
                client["id"],
                client["secret"],
                authorization_code=authorization_code,
                rely_on_oauth_basic=rely_on_oauth_basic,
                ask_for_long_token=ask_for_long_token,
                verbose=verbose,
            )
    return access_token


def get_headers(access_token: str | None = "") -> dict[str, str]:
    if access_token is None:
        access_token = ""

    headers = get_oauth_headers(access_token)
    if len(access_token) == 0:
        del headers["Authorization"]

    return headers


def get_cookies(
    authorization_code: str | None,
    access_token: str | None,
    verbose: bool = True,
) -> dict[str, str]:
    # References:
    # - https://github.com/woctezuma/egs-15DaysofGames/issues/3
    # - https://github.com/MixV2/EpicResearch/issues/89#issuecomment-1003520859

    if access_token is None or len(access_token) == 0:
        if authorization_code is None or len(authorization_code) == 0:
            cookies = {}
        else:
            cookies = {"EPIC_BEARER_TOKEN": authorization_code}
            if verbose:
                print("Using authorization code in a cookie field.")
    else:
        cookies = {"EPIC_BEARER_TOKEN": access_token}
        if verbose:
            print("Using access token in a cookie field.")

    return cookies


def get_simple_json_query() -> dict[str, str]:
    json_query = {
        "query": "{ Catalog { searchStore(count:3, start: 0) { paging {total} elements {title} } } }",
    }

    return json_query


def query_graphql_while_auth(
    target_client_name: str = "launcherAppClient2",
    rely_on_oauth_basic: bool = False,
    ask_for_long_token: bool = True,
    authorization_code: str = "",
    auth_clients_fname: str = None,
    verbose: bool = True,
) -> dict:
    client = load_target_auth_client(
        target_client_name,
        auth_clients_fname=auth_clients_fname,
        verbose=verbose,
    )

    _ = get_url_to_visit_for_auth_code(client["id"], verbose=verbose)

    access_token = get_token(
        client,
        authorization_code=authorization_code,
        rely_on_oauth_basic=rely_on_oauth_basic,
        ask_for_long_token=ask_for_long_token,
        verbose=verbose,
    )

    r = requests.post(
        url=get_egs_url(),
        json=get_simple_json_query(),
        headers=get_headers(access_token),
        cookies=get_cookies(authorization_code, access_token, verbose=verbose),
    )

    if r.ok:
        data = r.json()
    else:
        print(r.status_code)
        data = {}

    if verbose:
        print(data)

    return data


if __name__ == "__main__":
    parent_dir = "../"
    cookie_name = parent_dir + get_epic_cookie_file_name()
    auth_clients_fname = parent_dir + get_auth_client_filename()
    verbose = True

    target_client_name = "launcherAppClient2"
    rely_on_oauth_basic = False
    ask_for_long_token = True
    authorization_code = get_authorization_code(
        cookie_fname=cookie_name,
        verbose=verbose,
    )

    data = query_graphql_while_auth(
        target_client_name=target_client_name,
        rely_on_oauth_basic=rely_on_oauth_basic,
        ask_for_long_token=ask_for_long_token,
        authorization_code=authorization_code,
        auth_clients_fname=auth_clients_fname,
        verbose=verbose,
    )
