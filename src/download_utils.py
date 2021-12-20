import requests


def get_egs_url() -> str:
    return "https://www.epicgames.com/graphql"


def get_default_params() -> dict:
    params = {
        "category": '"games"',
        "count": 1000,
    }
    return params


def get_egs_query(cursor: int = 0, step: int = None, include_dlc: bool = False) -> str:
    params = get_default_params()

    if step is None:
        step = params["count"]

    if include_dlc:
        category_str = ""
    else:
        category_str = f'category: {params["category"]}, '

    prefix = "{Catalog {searchStore"
    param_str = f"({category_str}count: {step}, start: {cursor})"

    promo_template = "{promotionalOffers {startDate endDate discountSetting {discountType discountPercentage} } }"
    current_promo = f"promotionalOffers {promo_template}"
    upcoming_promo = f"upcomingPromotionalOffers {promo_template}"
    promo_str = "promotions {" + f"{current_promo} {upcoming_promo}" + "}"

    paging_str = "paging {count total}"
    element_str = "elements {" + f"title {promo_str}" + "}"

    content_str = "{" + f"{paging_str} {element_str}" + "}"
    suffix = "}}"

    query = prefix + param_str + content_str + suffix
    return query


def download_store_data(
        cursor: int = 0, step: int = None, include_dlc: bool = False, verbose: bool = True
) -> dict:
    if verbose:
        print(f"Cursor = {cursor} ; step = {step}")

    r = requests.post(
        url=get_egs_url(),
        json={
            "query": get_egs_query(cursor=cursor, step=step, include_dlc=include_dlc)
        },
    )

    if verbose:
        print(f"Status code = {r.status_code}")

    if r.ok:
        data = r.json()
        try:
            store_data = data["data"]["Catalog"]["searchStore"]
        except TypeError:
            # Retry in case data is None
            store_data = download_store_data(
                cursor=cursor, step=step, include_dlc=include_dlc, verbose=verbose
            )
    else:
        store_data = {}

    return store_data


if __name__ == "__main__":
    store_data = download_store_data(cursor=50, step=10)
