from unittest import TestCase

import src.aggregate_utils
import src.download_utils
import src.filter_utils
import src.io_utils
import src.print_utils


class TestAggregateUtilsMethods(TestCase):
    def test_extract_upcoming_promotions(self):
        store_data = {"elements": []}
        self.assertEqual(
            src.aggregate_utils.extract_upcoming_promotions(store_data), []
        )

    def test_extract_num_promos_from_metadata(self):
        store_data = {"paging": {"total": -1}}
        self.assertEqual(
            src.aggregate_utils.extract_num_promos_from_metadata(store_data), -1
        )

    def test_download_all_promos(self):
        all_promos = src.aggregate_utils.download_all_promos(verbose=True)
        self.assertGreater(len(all_promos), 0)


class TestDownloadUtilsMethods(TestCase):
    def test_get_egs_url(self):
        self.assertEqual(
            src.download_utils.get_egs_url(), "https://www.epicgames.com/graphql"
        )

    def test_get_default_params(self):
        params = src.download_utils.get_default_params()
        self.assertEqual(params["category"], '"games"')
        self.assertEqual(params["count"], 1000)

    def test_get_egs_query(self):
        query = src.download_utils.get_egs_query()
        self.assertIn("{Catalog {searchStore", query)
        self.assertIn("paging {count total}", query)

    def test_download_store_data(self):
        store_data = src.download_utils.download_store_data(
            cursor=0, step=1, verbose=True
        )
        self.assertIn("elements", store_data)
        self.assertIn("paging", store_data)


class TestFilterUtilsMethods(TestCase):
    def test_has_upcoming_promo(self):
        element = {
            "promotions": {"upcomingPromotionalOffers": ["this will be discounted!"]}
        }
        self.assertTrue(src.filter_utils.has_upcoming_promo(element))
        element = {"promotions": None}
        self.assertFalse(src.filter_utils.has_upcoming_promo(element))
        element = {"promotions": {"upcomingPromotionalOffers": []}}
        self.assertFalse(src.filter_utils.has_upcoming_promo(element))

    def test_filter_promos(self):
        promos = [
            {"promotions": {"upcomingPromotionalOffers": ["this will be discounted!"]}},
            {"promotions": None},
            {"promotions": {"upcomingPromotionalOffers": []}},
        ]
        expected_filtered_promos = [
            {"promotions": {"upcomingPromotionalOffers": ["this will be discounted!"]}}
        ]
        self.assertListEqual(
            src.filter_utils.filter_promos(promos), expected_filtered_promos
        )


class TestIOUtilsMethods(TestCase):
    def test_get_output_filename(self):
        self.assertEqual(src.io_utils.get_output_filename(), "data/promos.json")

    def test_load_promos(self):
        promos = src.io_utils.load_promos()
        self.assertGreater(len(promos), 0)

    def test_save_promos(self):
        promos = src.io_utils.load_promos()

        dummy_fname = "data/dummy_promos.json"
        src.io_utils.save_promos(promos, dummy_fname)
        dummy_promos = src.io_utils.load_promos(dummy_fname)

        self.assertListEqual(promos, dummy_promos)


class TestPrintUtilsMethods(TestCase):
    def test_get_sorted_promos(self):
        dummy_promos = [
            {
                "promotions": {
                    "upcomingPromotionalOffers": [
                        {"promotionalOffers": [{"startDate": 0, "endDate": 0}]}
                    ]
                }
            },
            {
                "promotions": {
                    "upcomingPromotionalOffers": [
                        {"promotionalOffers": [{"startDate": 0, "endDate": 1}]}
                    ]
                }
            },
            {
                "promotions": {
                    "upcomingPromotionalOffers": [
                        {"promotionalOffers": [{"startDate": 1, "endDate": 0}]}
                    ]
                }
            },
            {
                "promotions": {
                    "upcomingPromotionalOffers": [
                        {"promotionalOffers": [{"startDate": 1, "endDate": 1}]}
                    ]
                }
            },
        ]

        sorted_promos = src.print_utils.get_sorted_promos(dummy_promos)

        s = ""
        for i in range(len(sorted_promos)):
            s += str(
                sorted_promos[i]["promotions"]["upcomingPromotionalOffers"][0][
                    "promotionalOffers"
                ][0]["startDate"]
            )
            s += str(
                sorted_promos[i]["promotions"]["upcomingPromotionalOffers"][0][
                    "promotionalOffers"
                ][0]["endDate"]
            )

        self.assertEqual(s, "00100111")

    def test_get_meta_data(self):
        element = {
            "promotions": {
                "upcomingPromotionalOffers": [{"promotionalOffers": ["hello"]}]
            }
        }
        self.assertEqual(src.print_utils.get_meta_data(element), "hello")

    def test_trim_date(self):
        dummy_date = "2021-12-18T16:00:00.000Z"
        self.assertEqual(src.print_utils.trim_date(dummy_date), "2021-12-18 @ 16h")

    def test_extract_hour(self):
        dummy_date = "2021-12-18T16:00:00.000Z"
        self.assertEqual(src.print_utils.extract_hour(dummy_date), "16")

    def test_extract_day(self):
        dummy_date = "2021-12-18T16:00:00.000Z"
        self.assertEqual(src.print_utils.extract_day(dummy_date), "2021-12-18")

    def test_to_discount_symbol(self):
        self.assertEqual(src.print_utils.to_discount_symbol("PERCENTAGE"), "%")
        self.assertEqual(src.print_utils.to_discount_symbol("DUMMY_UNKNOWN"), "???")

    def test_print_promos(self):
        promos = src.io_utils.load_promos()
        filtered_promos = src.filter_utils.filter_promos(promos)
        self.assertTrue(src.print_utils.print_promos(filtered_promos))
