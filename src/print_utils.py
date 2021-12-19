from src.filter_utils import get_promo_str
from src.sort_utils import get_sorted_promos


def get_meta_data(element, check_upcoming_promos):
    """
    Gets meta data from promotion.

    args: element: dict, check_upcoming_promos: bool

    Returns: Meta data.
    """
    promo_str = get_promo_str(check_upcoming_promos)
    meta_data = element["promotions"][promo_str][0]["promotionalOffers"][0]

    return meta_data


def trim_date(date_str):
    """
    Trim date string.

    args: date_str: str

    Returns: Trimmed date string.
    """
    return f"{extract_day(date_str)} @ {extract_hour(date_str)}h"


def extract_hour(date_str):
    """
    Extract hour from date string.

    args: date_str: str

    Returns: Hour: int
    """
    return date_str[11:13]


def extract_day(date_str):
    """
    Extract day from date string.

    args: date_str: str

    returns: Day: str
    """
    return date_str[:10]


def to_discount_symbol(discount_type):
    """
    Turn discount type into symbol.

    args: discount_type: str

    Returns: Symbol: str
    """
    if discount_type == "PERCENTAGE":
        discount_symbol = "%"
    else:
        discount_symbol = "???"
    return discount_symbol


def print_promos(filtered_promos, check_upcoming_promos=True):
    """
    Print all promotions.

    args: filtered_promos: List[dict], check_upcoming_promos: bool

    Returns: True.
    """
    for e in get_sorted_promos(filtered_promos, check_upcoming_promos):
        name = e["title"]
        meta_data = get_meta_data(e, check_upcoming_promos)

        start_date = trim_date(meta_data["startDate"])
        end_date = trim_date(meta_data["endDate"])
        discount = meta_data["discountSetting"]["discountPercentage"]
        symbol = to_discount_symbol(
            meta_data["discountSetting"]["discountType"])

        print(
            f"- [ {discount:2d}{symbol} off ] {start_date} -> {end_date} : {name}")

    return True


if __name__ == "__main__":
    pass
