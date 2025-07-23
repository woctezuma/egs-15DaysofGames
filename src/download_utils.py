import requests


def get_egs_url() -> str:
    return "https://graphql.epicgames.com/ue/graphql"


def get_default_params() -> dict:
    params = {
        "category": '"games"',
        "count": 40,
    }
    return params


def get_egs_query(cursor: int = 0, step: int = None, include_dlc: bool = False) -> str:
    params = get_default_params()

    if step is None:
        step = params["count"]

    category_str = "" if include_dlc else f"category: {params['category']}, "

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
    cursor: int = 0,
    step: int = None,
    include_dlc: bool = False,
    auth_code: str = None,
    num_retries_left: int = 3,
    verbose: bool = True,
) -> dict:
    if verbose:
        print(f"Cursor = {cursor} ; step = {step}")

    json_data = {
        "query": get_egs_query(cursor=cursor, step=step, include_dlc=include_dlc),
    }

    if auth_code is not None:
        print(
            "[Warning] Authorization Code is directly used, without any Access Token. If possible, find a better way.",
        )
        json_data["code"] = auth_code

    r = requests.post(
        url=get_egs_url(),
        json=json_data,
    )

    if verbose:
        print(f"Status code = {r.status_code}")

    if r.ok:
        data = r.json()
        try:
            store_data = data["data"]["Catalog"]["searchStore"]
        except TypeError:
            if num_retries_left == 0:
                store_data = {}
            else:
                print(f"Retrying the download. {num_retries_left} tentatives left.")
                # Retry in case data is None
                store_data = download_store_data(
                    cursor=cursor,
                    step=step,
                    include_dlc=include_dlc,
                    auth_code=auth_code,
                    num_retries_left=num_retries_left - 1,
                    verbose=verbose,
                )
    else:
        store_data = {}

    return store_data


if __name__ == "__main__":
    store_data = download_store_data(cursor=50, step=10)
