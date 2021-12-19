from src.download_utils import get_default_params, download_store_data
from src.search_utils import find_title


def extract_upcoming_promotions(store_data: dict) -> list[dict]:
    promos = store_data["elements"]
    return promos


def extract_num_promos_from_metadata(store_data: dict) -> int:
    total_num_promos = store_data["paging"]["total"]
    return total_num_promos


def download_all_promos(verbose: bool = True) -> list[dict]:
    dummy_store_data = download_store_data(cursor=0, step=1, verbose=verbose)
    total_num_promos = extract_num_promos_from_metadata(dummy_store_data)

    if verbose:
        print(f"#promotions = {total_num_promos}")

    params = get_default_params()
    step = params["count"]

    all_promos = []

    for cursor in range(0, total_num_promos, step):
        store_data = download_store_data(cursor=cursor, step=step, verbose=verbose)
        promos = extract_upcoming_promotions(store_data)

        all_promos += promos

    return all_promos


if __name__ == "__main__":
    store_data = download_store_data(cursor=1000)
    promos = extract_upcoming_promotions(store_data)

    target_game_name = "Prey"
    element = find_title(promos, target_game_name, verbose=True)
