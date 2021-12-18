import requests


def get_egs_url():
    return "https://www.epicgames.com/graphql"


def get_default_params():
    params = {
        "category": '"games"',
        "count": 1000,
    }
    return params


def get_egs_query(cursor=0, step=None):
    params = get_default_params()

    if step is None:
        step = params["count"]

    prefix = "{Catalog {searchStore"
    param_str = f'(category: {params["category"]}, count: {step}, start: {cursor})'
    suffix = " {paging {count total} elements {title promotions {upcomingPromotionalOffers {promotionalOffers {startDate endDate discountSetting {discountType discountPercentage} } } } } } } }"

    query = prefix + param_str + suffix
    return query


def download_store_data(cursor=0, step=None, verbose=True):
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