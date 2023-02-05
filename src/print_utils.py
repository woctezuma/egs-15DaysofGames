from src.filter_utils import get_promo_str
from src.sort_utils import get_sorted_promos


def get_meta_data(element: dict[str, dict], check_upcoming_promos: bool) -> list[dict]:
    promo_str = get_promo_str(check_upcoming_promos)
    meta_data = element["promotions"][promo_str][0]["promotionalOffers"]

    return meta_data


def trim_date(date_str: str) -> str:
    return f"{extract_day(date_str)} @ {extract_hour(date_str)}h"


def extract_hour(date_str: str) -> str:
    return date_str[11:13]


def extract_day(date_str: str) -> str:
    return date_str[:10]


def to_discount_value(price_multiplier_in_percent: int) -> int:
    discount_value = 100 - price_multiplier_in_percent
    return discount_value


def to_discount_symbol(discount_type: str) -> str:
    if discount_type == "PERCENTAGE":
        discount_symbol = "%"
    else:
        discount_symbol = "???"
    return discount_symbol


def print_promos(
    filtered_promos: list[dict],
    check_upcoming_promos: bool = True,
) -> bool:
    for e in get_sorted_promos(filtered_promos, check_upcoming_promos):
        name = e["title"]
        meta_data = get_meta_data(e, check_upcoming_promos)

        for promotional_offer in meta_data:
            start_date = trim_date(promotional_offer["startDate"])
            end_date = trim_date(promotional_offer["endDate"])
            discount = to_discount_value(
                promotional_offer["discountSetting"]["discountPercentage"],
            )
            symbol = to_discount_symbol(
                promotional_offer["discountSetting"]["discountType"],
            )

            print(
                f"- [ {discount:3d}{symbol} off ] {start_date} -> {end_date} : {name}",
            )

    return True
