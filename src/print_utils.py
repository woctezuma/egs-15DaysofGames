def get_sorted_promos(promos):
    sorted_promos = sorted(
        promos,
        key=lambda x: (
            x["promotions"]["upcomingPromotionalOffers"][0]["promotionalOffers"][0][
                "endDate"
            ],
            x["promotions"]["upcomingPromotionalOffers"][0]["promotionalOffers"][0][
                "startDate"
            ],
        ),
    )
    return sorted_promos


def get_meta_data(element):
    meta_data = element["promotions"]["upcomingPromotionalOffers"][0][
        "promotionalOffers"
    ][0]

    return meta_data


def trim_date(date_str):
    return date_str[:10]


def print_promos(filtered_promos):
    for e in get_sorted_promos(filtered_promos):
        name = e["title"]
        meta_data = get_meta_data(e)

        start_date = trim_date(meta_data["startDate"])
        end_date = trim_date(meta_data["endDate"])
        discount = meta_data["discountSetting"]["discountPercentage"]

        print(f"- [ {discount:2d}% off ] {start_date} -> {end_date} : {name}")

    return


if __name__ == "__main__":
    pass
