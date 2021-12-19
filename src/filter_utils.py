def get_promo_str(check_upcoming_promos: bool) -> str:
    if check_upcoming_promos:
        promo_str = "upcomingPromotionalOffers"
    else:
        promo_str = "promotionalOffers"
    return promo_str


def is_relevant_promo(element: dict[str, dict], check_upcoming_promos: bool) -> bool:
    promo_str = get_promo_str(check_upcoming_promos)
    flag = (
            element["promotions"] is not None
            and promo_str in element["promotions"]
            and len(element["promotions"][promo_str]) > 0
    )

    return flag


def has_current_promo(element: dict[str, dict]) -> bool:
    return is_relevant_promo(element, check_upcoming_promos=False)


def has_upcoming_promo(element: dict[str, dict]) -> bool:
    return is_relevant_promo(element, check_upcoming_promos=True)


def filter_promos(promos: list[dict], check_upcoming_promos: bool = True) -> list[dict]:
    filtered_promos = [e for e in promos if is_relevant_promo(e, check_upcoming_promos)]

    return filtered_promos


if __name__ == "__main__":
    pass
