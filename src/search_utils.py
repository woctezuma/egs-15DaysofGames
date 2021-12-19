def find_title(promos: list[dict], target_game_name: str, verbose: bool = True) -> dict:
    target_game_name_lowercase = target_game_name.lower()

    result = None

    for e in promos:
        if target_game_name_lowercase in e["title"].lower():
            result = e
            break

    if verbose:
        print(result)

    return result


if __name__ == "__main__":
    pass
