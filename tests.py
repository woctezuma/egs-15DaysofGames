from unittest import TestCase

import src.aggregate_utils
import src.auth_utils
import src.download_utils
import src.filter_utils
import src.io_utils
import src.print_utils
import src.search_utils
import src.sort_utils
import src.token_utils


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
        for include_dlc in [False, True]:
            all_promos = src.aggregate_utils.download_all_promos(
                include_dlc=include_dlc, verbose=True
            )
            self.assertGreater(len(all_promos), 0)


class TestDownloadUtilsMethods(TestCase):
    def test_get_egs_url(self):
        self.assertEqual(
            src.download_utils.get_egs_url(), "https://graphql.epicgames.com/graphql"
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
        for include_dlc in [False, True]:
            store_data = src.download_utils.download_store_data(
                cursor=0, step=1, include_dlc=include_dlc, verbose=True
            )
            self.assertIn("elements", store_data)
            self.assertIn("paging", store_data)


class TestFilterUtilsMethods(TestCase):
    def get_dummy_current_promo(self):
        element = {
            "promotions": {"promotionalOffers": ["this is currently discounted!"]}
        }
        return element

    def get_dummy_upcoming_promo(self):
        element = {
            "promotions": {"upcomingPromotionalOffers": ["this will be discounted!"]}
        }
        return element

    def test_get_promo_str(self):
        self.assertEqual(
            src.filter_utils.get_promo_str(check_upcoming_promos=True),
            "upcomingPromotionalOffers",
        )
        self.assertEqual(
            src.filter_utils.get_promo_str(check_upcoming_promos=False),
            "promotionalOffers",
        )

    def test_is_relevant_promo(self):
        element = self.get_dummy_current_promo()
        self.assertFalse(src.filter_utils.is_relevant_promo(element, True))
        self.assertTrue(src.filter_utils.is_relevant_promo(element, False))
        element = self.get_dummy_upcoming_promo()
        self.assertTrue(src.filter_utils.is_relevant_promo(element, True))
        self.assertFalse(src.filter_utils.is_relevant_promo(element, False))

    def test_has_current_promo(self):
        element = self.get_dummy_current_promo()
        self.assertTrue(src.filter_utils.has_current_promo(element))
        element = self.get_dummy_upcoming_promo()
        self.assertFalse(src.filter_utils.has_current_promo(element))
        element = {"promotions": None}
        self.assertFalse(src.filter_utils.has_current_promo(element))
        element = {"promotions": {"promotionalOffers": []}}
        self.assertFalse(src.filter_utils.has_current_promo(element))
        element = {"promotions": {"upcomingPromotionalOffers": []}}
        self.assertFalse(src.filter_utils.has_current_promo(element))

    def test_has_upcoming_promo(self):
        element = self.get_dummy_current_promo()
        self.assertFalse(src.filter_utils.has_upcoming_promo(element))
        element = self.get_dummy_upcoming_promo()
        self.assertTrue(src.filter_utils.has_upcoming_promo(element))
        element = {"promotions": None}
        self.assertFalse(src.filter_utils.has_upcoming_promo(element))
        element = {"promotions": {"promotionalOffers": []}}
        self.assertFalse(src.filter_utils.has_upcoming_promo(element))
        element = {"promotions": {"upcomingPromotionalOffers": []}}
        self.assertFalse(src.filter_utils.has_upcoming_promo(element))

    def test_filter_promos(self):
        promos = [
            self.get_dummy_current_promo(),
            self.get_dummy_upcoming_promo(),
            {"promotions": None},
            {"promotions": {"promotionalOffers": []}},
            {"promotions": {"upcomingPromotionalOffers": []}},
        ]
        expected_filtered_promos = [
            self.get_dummy_upcoming_promo(),
        ]
        self.assertListEqual(
            src.filter_utils.filter_promos(promos, check_upcoming_promos=True),
            expected_filtered_promos,
        )
        expected_filtered_promos = [
            self.get_dummy_current_promo(),
        ]
        self.assertListEqual(
            src.filter_utils.filter_promos(promos, check_upcoming_promos=False),
            expected_filtered_promos,
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

    def test_get_auth_client_filename(self):
        self.assertEqual(
            src.io_utils.get_auth_client_filename(), "data/auth_clients.json"
        )

    def test_load_auth_clients(self):
        auth_clients = src.io_utils.load_auth_clients()
        self.assertGreater(len(auth_clients), 0)

    def test_load_target_auth_client(self):
        target_client = src.io_utils.load_target_auth_client(
            target_client_name="dummy", verbose=True
        )
        self.assertEqual(len(target_client), 0)
        target_client = src.io_utils.load_target_auth_client(
            target_client_name="fortnitePCGameClient", verbose=True
        )
        self.assertEqual(len(target_client), 3)
        self.assertEqual(target_client["name"], "fortnitePCGameClient")
        self.assertEqual(target_client["id"], "ec684b8c687f479fadea3cb2ad83f5c6")
        self.assertEqual(target_client["secret"], "e1f31c211f28413186262d37a13fc84d")
        target_client = src.io_utils.load_target_auth_client(
            target_client_name="graphqlWebsite", verbose=True
        )
        self.assertEqual(len(target_client), 3)
        self.assertEqual(target_client["name"], "graphqlWebsite")
        self.assertEqual(target_client["id"], "319e1527d0be4457a1067829fc0ad86e")
        self.assertEqual(target_client["secret"], None)


class TestSortUtilsMethods(TestCase):
    def test_sanitize_promos(self):
        for promo_str in ["upcomingPromotionalOffers", "promotionalOffers"]:
            l = [
                {
                    "promotions": {
                        promo_str: [
                            {
                                "promotionalOffers": [
                                    {"endDate": None, "startDate": "world"}
                                ]
                            }
                        ]
                    }
                },
                {
                    "promotions": {
                        promo_str: [
                            {
                                "promotionalOffers": [
                                    {"endDate": "hello", "startDate": "world"}
                                ]
                            }
                        ]
                    }
                },
                {
                    "promotions": {
                        promo_str: [
                            {
                                "promotionalOffers": [
                                    {"endDate": "hello", "startDate": None}
                                ]
                            }
                        ]
                    }
                },
                {
                    "promotions": {
                        promo_str: [
                            {
                                "promotionalOffers": [
                                    {"endDate": None, "startDate": None}
                                ]
                            }
                        ]
                    }
                },
            ]
            s = src.sort_utils.sanitize_promos(l)
            expected_results = [
                {"endDate": "N/A", "startDate": "world"},
                {"endDate": "hello", "startDate": "world"},
                {"endDate": "hello", "startDate": "N/A"},
                {"endDate": "N/A", "startDate": "N/A"},
            ]
            for (e, expected_output) in zip(s, expected_results):
                for date_bound in ["endDate", "startDate"]:
                    output = e["promotions"][promo_str][0]["promotionalOffers"][0]
                    self.assertEqual(
                        output[date_bound],
                        expected_output[date_bound],
                    )

    def test_get_sorted_promos(self):
        for check_upcoming_promos in [True, False]:
            promo_str = src.filter_utils.get_promo_str(check_upcoming_promos)

            dummy_promos = [
                {
                    "promotions": {
                        promo_str: [
                            {"promotionalOffers": [{"startDate": 0, "endDate": 0}]}
                        ]
                    }
                },
                {
                    "promotions": {
                        promo_str: [
                            {"promotionalOffers": [{"startDate": 0, "endDate": 1}]}
                        ]
                    }
                },
                {
                    "promotions": {
                        promo_str: [
                            {"promotionalOffers": [{"startDate": 1, "endDate": 0}]}
                        ]
                    }
                },
                {
                    "promotions": {
                        promo_str: [
                            {"promotionalOffers": [{"startDate": 1, "endDate": 1}]}
                        ]
                    }
                },
            ]

            sorted_promos = src.sort_utils.get_sorted_promos(
                dummy_promos, check_upcoming_promos
            )

            s = ""
            for element in sorted_promos:
                calendar = element["promotions"][promo_str][0]["promotionalOffers"][0]
                s += str(calendar["startDate"])
                s += str(calendar["endDate"])

            self.assertEqual(s, "00100111")


class TestPrintUtilsMethods(TestCase):
    def test_get_meta_data(self):
        element = {
            "promotions": {
                "upcomingPromotionalOffers": [{"promotionalOffers": ["hello"]}]
            }
        }
        self.assertEqual(src.print_utils.get_meta_data(element, True), "hello")
        element = {
            "promotions": {"promotionalOffers": [{"promotionalOffers": ["hello"]}]}
        }
        self.assertEqual(src.print_utils.get_meta_data(element, False), "hello")

    def test_trim_date(self):
        dummy_date = "2021-12-18T16:00:00.000Z"
        self.assertEqual(src.print_utils.trim_date(dummy_date), "2021-12-18 @ 16h")

    def test_extract_hour(self):
        dummy_date = "2021-12-18T16:00:00.000Z"
        self.assertEqual(src.print_utils.extract_hour(dummy_date), "16")

    def test_extract_day(self):
        dummy_date = "2021-12-18T16:00:00.000Z"
        self.assertEqual(src.print_utils.extract_day(dummy_date), "2021-12-18")

    def test_to_discount_value(self):
        for r in range(0, 101, 25):
            self.assertEqual(100 - r, src.print_utils.to_discount_value(r))

    def test_to_discount_symbol(self):
        self.assertEqual(src.print_utils.to_discount_symbol("PERCENTAGE"), "%")
        self.assertEqual(src.print_utils.to_discount_symbol("DUMMY_UNKNOWN"), "???")

    def test_print_promos(self):
        promos = src.io_utils.load_promos()
        for check_upcoming_promos in [True, False]:
            filtered_promos = src.filter_utils.filter_promos(
                promos, check_upcoming_promos=check_upcoming_promos
            )
            self.assertTrue(
                src.print_utils.print_promos(
                    filtered_promos, check_upcoming_promos=check_upcoming_promos
                )
            )


class TestSearchUtilsMethods(TestCase):
    def test_find_title(self):
        promos = src.io_utils.load_promos()
        target_game_name = "Prey"
        element = src.search_utils.find_title(promos, target_game_name, verbose=True)
        self.assertIsNotNone(element)
        self.assertIn(target_game_name, element["title"])

    def test_find_title_regex(self):
        promos = src.io_utils.load_promos()
        target_game_name = "Prey"
        matches = src.search_utils.find_title_regex(
            promos, target_game_name, verbose=True
        )
        self.assertIsNotNone(matches)
        self.assertGreater(len(matches), 0)
        for element in matches:
            self.assertIn(target_game_name, element["title"])


class TestAuthUtilsMethods(TestCase):
    def test_get_egs_auth_url(self):
        self.assertEqual(
            src.auth_utils.get_egs_auth_url(),
            "https://www.epicgames.com/id/api/redirect",
        )

    def test_get_auth_client(self):
        client = src.auth_utils.get_auth_client()
        self.assertIn("name", client.keys())
        self.assertIn("id", client.keys())
        self.assertIn("secret", client.keys())
        self.assertIsNotNone(client["name"])
        self.assertIsNotNone(client["id"])

    def test_get_url_to_visit_for_auth_code(self):
        self.assertIn(
            src.auth_utils.get_egs_auth_url(),
            src.auth_utils.get_url_to_visit_for_auth_code(),
        )
        self.assertIn("?clientId=", src.auth_utils.get_url_to_visit_for_auth_code())
        self.assertIn(
            "&responseType=code", src.auth_utils.get_url_to_visit_for_auth_code()
        )


class TestTokenUtilsMethods(TestCase):
    def test_get_egs_hosts(self):
        egs_hosts = src.token_utils.get_egs_hosts()
        self.assertGreater(len(egs_hosts), 0)
        self.assertEqual(
            egs_hosts["_oauth_host"], "account-public-service-prod.ol.epicgames.com"
        )

    def test_get_egs_oauth_url(self):
        url = src.token_utils.get_egs_oauth_url()
        self.assertEqual(
            url,
            "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
        )

    def test_encode_in_base64(self):
        # Reference: https://www.base64encode.org/
        self.assertEqual(
            src.token_utils.encode_in_base64("hello world"), "aGVsbG8gd29ybGQ="
        )
        self.assertEqual(
            src.token_utils.encode_in_base64("hello:world"), "aGVsbG86d29ybGQ="
        )

    def test_convert_to_base64_secret(self):
        client_id = "hello"
        client_secret = "world"
        expected_base64_secret = src.token_utils.encode_in_base64(
            f"{client_id}:{client_secret}"
        )
        self.assertEqual(
            src.token_utils.convert_to_base64_secret(
                client_id=client_id, client_secret=client_secret
            ),
            expected_base64_secret,
        )
        # Reference: https://github.com/MixV2/EpicResearch/blob/master/docs/auth/grant_types/authorization_code.md
        self.assertEqual(
            src.token_utils.convert_to_base64_secret(
                client_id="ec684b8c687f479fadea3cb2ad83f5c6",
                client_secret="e1f31c211f28413186262d37a13fc84d",
            ),
            "ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=",
        )

    def test_get_secret_headers(self):
        client_id = "hello"
        client_secret = "world"
        headers = src.token_utils.get_secret_headers(
            client_id=client_id, client_secret=client_secret
        )
        base64_secret = src.token_utils.convert_to_base64_secret(
            client_id=client_id, client_secret=client_secret
        )
        self.assertIn("Content-Type", headers.keys())
        self.assertEqual(headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertIn("Authorization", headers.keys())
        self.assertEqual(headers["Authorization"], f"basic {base64_secret}")

    def test_get_access_token(self):
        access_token = src.token_utils.get_access_token(
            client_id="hello",
            client_secret="world",
            body_data={"grant_type": "dummy"},
            verbose=True,
        )
        self.assertIsNone(access_token)

    def test_get_access_token_with_client_credentials(self):
        access_token = src.token_utils.get_access_token_with_client_credentials(
            client_id="hello", client_secret="world", verbose=True
        )
        self.assertIsNone(access_token)
        # Reference: https://github.com/MixV2/EpicResearch/blob/master/docs/auth/grant_types/authorization_code.md
        access_token = src.token_utils.get_access_token_with_client_credentials(
            client_id="ec684b8c687f479fadea3cb2ad83f5c6",
            client_secret="e1f31c211f28413186262d37a13fc84d",
            verbose=True,
        )
        self.assertIsNotNone(access_token)
        self.assertGreater(len(access_token), 0)
        self.assertEqual(len(access_token), 32)

    def test_get_access_token_with_authorization_code(self):
        access_token = src.token_utils.get_access_token_with_authorization_code(
            client_id="hello",
            client_secret="world",
            authorization_code="dummy",
            verbose=True,
        )
        self.assertIsNone(access_token)

    def test_get_oauth_headers(self):
        headers = src.token_utils.get_oauth_headers(access_token="dummy_token")
        self.assertIn("Accept", headers.keys())
        self.assertEqual(headers["Accept"], "application/json")
        self.assertIn("Content-Type", headers.keys())
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertIn("Authorization", headers.keys())
        self.assertEqual(headers["Authorization"], "Bearer dummy_token")
