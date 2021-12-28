import json


def get_output_filename() -> str:
    fname = "data/promos.json"
    return fname


def load_promos(fname: str = None) -> list[dict]:
    if fname is None:
        fname = get_output_filename()

    with open(fname, "r", encoding="utf8") as f:
        data = json.load(f)

    return data


def save_promos(data: list[dict], fname: str = None) -> None:
    if fname is None:
        fname = get_output_filename()

    with open(fname, "w", encoding="utf8") as f:
        json.dump(data, f)

    return


def get_auth_client_filename() -> str:
    fname = "data/auth_clients.json"
    return fname


def load_auth_clients() -> list[dict[str, str | None]]:
    fname = get_auth_client_filename()

    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


if __name__ == "__main__":
    fname = get_output_filename()
    print(fname)
