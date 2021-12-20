from src.filter_utils import get_promo_str


def sanitize_promos(promos: list[dict]) -> list[dict]:
    sanitized_promos = []

    for e in promos:
        for s in e["promotions"]:
            if len(e["promotions"][s]) == 0:
                continue
            for date_bound in ["endDate", "startDate"]:
                if e["promotions"][s][0]["promotionalOffers"][0][date_bound] is None:
                    e["promotions"][s][0]["promotionalOffers"][0][date_bound] = "N/A"
        sanitized_promos.append(e)

    return sanitized_promos


def get_sorted_promos(promos: list[dict], check_upcoming_promos: bool) -> list[dict]:
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
