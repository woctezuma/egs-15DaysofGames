import requests


def get_egs_url():
    """
    URL for EGS API.
    """
    return "https://www.epicgames.com/graphql"


def get_default_params():
    """
    Default parameters for EGS API.

    Returns: dict
    """
    params = {
        "category": '"games"',
        "count": 1000,
    }
    return params


def get_egs_query(cursor=0, step=None):
    """
    Get EGS query.

    args: cursor: int, step: int

    Returns query.
    """
    params = get_default_params()

    if step is None:
        step = params["count"]

    prefix = "{Catalog {searchStore"
    param_str = f'(category: {params["category"]}, count: {step}, start: {cursor})'

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


def download_store_data(cursor=0, step=None, verbose=True):
    """
    Downloads store data.

    args: cursor: int, step: int, verbose: bool

    Returns store data.
    """
    if verbose:
        print(f"Cursor = {cursor} ; step = {step}")

    r = requests.post(
        url=get_egs_url(),
        json={"query": get_egs_query(cursor=cursor, step=step)},
    )

    if verbose:
        print(f"Status code = {r.status_code}")

    if r.ok:
        data = r.json()
        try:
            store_data = data["data"]["Catalog"]["searchStore"]
        except TypeError:
            # Retry in case data is None
            store_data = download_store_data(cursor=cursor, verbose=verbose)
    else:
        store_data = {}

    return store_data


if __name__ == "__main__":
    store_data = download_store_data(cursor=50, step=10)
