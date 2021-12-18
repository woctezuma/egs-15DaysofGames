def has_upcoming_promo(element):
    flag = (
            element["promotions"] is not None
            and len(element["promotions"]["upcomingPromotionalOffers"]) > 0
    )

    return flag


def filter_promos(promos):
    filtered_promos = [e for e in promos if has_upcoming_promo(e)]

    return filtered_promos


if __name__ == "__main__":
    pass
