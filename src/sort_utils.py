from src.filter_utils import get_promo_str


def sanitize_promos(promos):
    sanitized_promos = []

    for e in promos:
        for s in e["promotions"]:
            if e["promotions"][s][0]["promotionalOffers"][0]["endDate"] is None:
                e["promotions"][s][0]["promotionalOffers"][0]["endDate"] = "N/A"
        sanitized_promos.append(e)

    return sanitized_promos


def get_sorted_promos(promos, check_upcoming_promos):
    promo_str = get_promo_str(check_upcoming_promos)

    sanitized_promos = sanitize_promos(promos)

    sorted_promos = sorted(
        sanitized_promos,
        key=lambda x: (
            x["promotions"][promo_str][0]["promotionalOffers"][0]["endDate"],
            x["promotions"][promo_str][0]["promotionalOffers"][0]["startDate"],
        ),
    )
    return sorted_promos
