from download_utils import get_default_params, download_store_data
import re


def extract_upcoming_promotions(store_data):
    """
    Extract upcoming promotions from store data.

    args: store_data: dict

    Returns: List of upcoming promotions.
    """
    promos = store_data["elements"]
    return promos


def extract_num_promos_from_metadata(store_data):
    """
    Extract number of promotions from metadata.

    args: store_data: dict

    Returns: Total number of promotions.
    """
    total_num_promos = store_data["paging"]["total"]
    return total_num_promos


def download_all_promos(verbose=True):
    """
    Download all promotions from store.

    args: promotions: verbose: bool

    Returns all promotions.
    """
    dummy_store_data = download_store_data(cursor=0, step=1, verbose=verbose)
    total_num_promos = extract_num_promos_from_metadata(dummy_store_data)

    if verbose:
        print(f"#promotions = {total_num_promos}")

    params = get_default_params()
    step = params["count"]

    all_promos = []

    for cursor in range(0, total_num_promos, step):
        store_data = download_store_data(
            cursor=cursor, step=step, verbose=verbose)
        promos = extract_upcoming_promotions(store_data)

        all_promos += promos

    return all_promos


def find_title(promotions, title):
    """
    Search for title in promotions.

    args: promotions: List[dict], title: str

    Returns: First potential match.
    """
    title = title.lower()
    for e in promotions:
        if title in e["title"].lower():
            print(e)
            return e


def find_title_regex(promotions, title):
    """
    Regex search for title in promotions.

    args: promotions: List[dict], title: str

    Returns: All potential matches.
    """
    return [e for e in promotions if title in re.search(title, e["title"], re.IGNORECASE)]


if __name__ == "__main__":
    store_data = download_store_data(cursor=1000)
    promos = extract_upcoming_promotions(store_data)

    target_game_name = "Prey"
    title_discount_details = find_title_regex(
        promotions=promos, title=target_game_name)
