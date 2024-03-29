import json
from pathlib import Path


def get_output_filename() -> str:
    fname = "data/promos.json"
    return fname


def load_promos(fname: str = None) -> list[dict]:
    if fname is None:
        fname = get_output_filename()

    with Path(fname).open(encoding="utf8") as f:
        data = json.load(f)

    return data


def save_promos(data: list[dict], fname: str = None) -> None:
    if fname is None:
        fname = get_output_filename()

    with Path(fname).open("w", encoding="utf8") as f:
        json.dump(data, f)

    return


def get_auth_client_filename() -> str:
    fname = "data/auth_clients.json"
    return fname


def load_auth_clients(fname: str = None) -> list[dict[str, str | None]]:
    if fname is None:
        fname = get_auth_client_filename()

    with Path(fname).open(encoding="utf-8") as f:
        data = json.load(f)

    return data


def load_target_auth_client(
    target_client_name: str = "launcherAppClient2",
    auth_clients_fname: str = None,
    verbose: bool = True,
) -> dict[str, str | None]:
    auth_clients = load_auth_clients(fname=auth_clients_fname)
    relevant_clients = [c for c in auth_clients if c["name"] == target_client_name]

    first_client = relevant_clients[0] if len(relevant_clients) > 0 else {}

    if verbose:
        print(first_client)

    return first_client


def get_epic_cookie_file_name() -> str:
    epic_cookie_file_name = "data/personal_info.json"

    return epic_cookie_file_name


def load_epic_cookie_from_disk(fname: str = None) -> dict[str, str]:
    if fname is None:
        fname = get_epic_cookie_file_name()

    try:
        with Path(fname).open(encoding="utf-8") as f:
            cookie = json.load(f)
    except FileNotFoundError:
        cookie = {}

    return cookie


if __name__ == "__main__":
    fname = get_output_filename()
    print(fname)
