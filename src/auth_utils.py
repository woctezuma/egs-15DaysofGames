import requests

from src.auth_code_utils import get_url_to_visit_for_auth_code, get_authorization_code
from src.auth_token_utils import (
    get_access_token_with_authorization_code,
    get_access_token_with_client_credentials,
    get_oauth_headers,
)
from src.download_utils import get_egs_url
from src.io_utils import (
    load_target_auth_client,
    get_epic_cookie_file_name,
    get_auth_client_filename,
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


def get_simple_json_query() -> dict[str, str]:
    json_query = dict(
        query="{ Catalog { searchStore(count:3, start: 0) { paging {total} elements {title} } } }"
    )

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
        target_client_name, auth_clients_fname=auth_clients_fname, verbose=verbose
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

    target_client_name = "launcherAppClient2"
    ask_for_long_token = True
    rely_on_oauth_basic = False
    authorization_code = get_authorization_code(cookie_fname=cookie_name, verbose=True)
    verbose = True

    data = query_graphql_while_auth(
        target_client_name=target_client_name,
        ask_for_long_token=ask_for_long_token,
        rely_on_oauth_basic=rely_on_oauth_basic,
        authorization_code=authorization_code,
        auth_clients_fname=auth_clients_fname,
        verbose=verbose,
    )
