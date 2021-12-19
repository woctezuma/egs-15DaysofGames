import re


def find_title(promos: list[dict], target_game_name: str, verbose: bool = True) -> dict:
    """Search for the first match of a game title."""
    target_game_name_lowercase = target_game_name.lower()

    result = None

    for e in promos:
        if target_game_name_lowercase in e["title"].lower():
            result = e
            break

    if verbose:
        print(result)

    return result


def find_title_regex(
    promos: list[dict], target_game_name: str, verbose: bool = True
) -> list[dict]:
    """Regex search for all matches of a game title. Credits to KonScanner."""
    matches = [
        e
        for e in promos
        if target_game_name in re.search(target_game_name, e["title"], re.IGNORECASE)
    ]

    if verbose:
        print(matches)

    return matches


if __name__ == "__main__":
    pass
