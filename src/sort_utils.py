from src.filter_utils import get_promo_str


def get_sorted_promos(promos, check_upcoming_promos):
    promo_str = get_promo_str(check_upcoming_promos)

    sorted_promos = sorted(
        promos,
        key=lambda x: (
            x["promotions"][promo_str][0]["promotionalOffers"][0]["endDate"],
            x["promotions"][promo_str][0]["promotionalOffers"][0]["startDate"],
        ),
    )
    return sorted_promos
