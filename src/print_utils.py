from src.filter_utils import get_promo_str
from src.sort_utils import get_sorted_promos


def get_meta_data(element, check_upcoming_promos):
    promo_str = get_promo_str(check_upcoming_promos)
    meta_data = element["promotions"][promo_str][0]["promotionalOffers"][0]

    return meta_data


def trim_date(date_str):
    return f"{extract_day(date_str)} @ {extract_hour(date_str)}h"


def extract_hour(date_str):
    return date_str[11:13]


def extract_day(date_str):
    return date_str[:10]


def to_discount_symbol(discount_type):
    if discount_type == "PERCENTAGE":
        discount_symbol = "%"
    else:
        discount_symbol = "???"
    return discount_symbol


def print_promos(filtered_promos, check_upcoming_promos=True):
    for e in get_sorted_promos(filtered_promos, check_upcoming_promos):
        name = e["title"]
        meta_data = get_meta_data(e, check_upcoming_promos)

        start_date = trim_date(meta_data["startDate"])
        end_date = trim_date(meta_data["endDate"])
        discount = meta_data["discountSetting"]["discountPercentage"]
        symbol = to_discount_symbol(meta_data["discountSetting"]["discountType"])

        print(f"- [ {discount:2d}{symbol} off ] {start_date} -> {end_date} : {name}")

    return True


if __name__ == "__main__":
    pass
