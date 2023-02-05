from src.auth_code_utils import get_authorization_code
from src.auth_utils import query_graphql_while_auth

if __name__ == "__main__":
    target_client_name = "launcherAppClient2"
    authorization_code = get_authorization_code()

    data = query_graphql_while_auth(
        target_client_name=target_client_name,
        authorization_code=authorization_code,
    )
