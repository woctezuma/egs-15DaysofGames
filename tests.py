from unittest import TestCase

import src.aggregate_utils
import src.auth_code_utils
import src.auth_token_utils
import src.auth_utils
import src.download_utils
import src.filter_utils
import src.io_utils
import src.print_utils
import src.search_utils
import src.sort_utils


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

    def test_get_epic_cookie_file_name(self):
        self.assertEqual(
            src.io_utils.get_epic_cookie_file_name(), "data/personal_info.json"
        )

    def test_load_epic_cookie_from_disk(self):
        cookie = src.io_utils.load_epic_cookie_from_disk(fname="dummy_cookie.json")
        self.assertEqual(len(cookie), 0)
        cookie = src.io_utils.load_epic_cookie_from_disk()
        self.assertGreaterEqual(len(cookie), 0)


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
        self.assertEqual(src.print_utils.get_meta_data(element, True), ["hello"])
        element = {
            "promotions": {"promotionalOffers": [{"promotionalOffers": ["hello"]}]}
        }
        self.assertEqual(src.print_utils.get_meta_data(element, False), ["hello"])

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


class TestAuthCodeUtilsMethods(TestCase):
    def test_get_egs_auth_url(self):
        self.assertEqual(
            src.auth_code_utils.get_egs_auth_url(),
            "https://www.epicgames.com/id/api/redirect",
        )

    def test_get_auth_client(self):
        client = src.auth_code_utils.get_auth_client()
        self.assertIn("name", client.keys())
        self.assertIn("id", client.keys())
        self.assertIn("secret", client.keys())
        self.assertIsNotNone(client["name"])
        self.assertIsNotNone(client["id"])

    def test_get_url_to_visit_for_auth_code(self):
        self.assertIn(
            src.auth_code_utils.get_egs_auth_url(),
            src.auth_code_utils.get_url_to_visit_for_auth_code(),
        )
        self.assertIn(
            "?clientId=", src.auth_code_utils.get_url_to_visit_for_auth_code()
        )
        self.assertIn(
            "&responseType=code", src.auth_code_utils.get_url_to_visit_for_auth_code()
        )

    def test_get_authorization_code(self):
        authorization_code = src.auth_code_utils.get_authorization_code(
            cookie_fname="dummy.json"
        )
        self.assertEqual(len(authorization_code), 0)
        authorization_code = src.auth_code_utils.get_authorization_code()
        self.assertGreaterEqual(len(authorization_code), 0)


class TestAuthTokenUtilsMethods(TestCase):
    def test_get_egs_hosts(self):
        egs_hosts = src.auth_token_utils.get_egs_hosts()
        self.assertGreater(len(egs_hosts), 0)
        self.assertEqual(
            egs_hosts["_oauth_host"], "account-public-service-prod.ol.epicgames.com"
        )

    def test_get_egs_oauth_url(self):
        url = src.auth_token_utils.get_egs_oauth_url()
        self.assertEqual(
            url,
            "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
        )

    def test_encode_in_base64(self):
        # Reference: https://www.base64encode.org/
        self.assertEqual(
            src.auth_token_utils.encode_in_base64("hello world"), "aGVsbG8gd29ybGQ="
        )
        self.assertEqual(
            src.auth_token_utils.encode_in_base64("hello:world"), "aGVsbG86d29ybGQ="
        )

    def test_convert_to_base64_secret(self):
        client_id = "hello"
        client_secret = "world"
        expected_base64_secret = src.auth_token_utils.encode_in_base64(
            f"{client_id}:{client_secret}"
        )
        self.assertEqual(
            src.auth_token_utils.convert_to_base64_secret(
                client_id=client_id, client_secret=client_secret
            ),
            expected_base64_secret,
        )
        # Reference: https://github.com/MixV2/EpicResearch/blob/master/docs/auth/grant_types/authorization_code.md
        self.assertEqual(
            src.auth_token_utils.convert_to_base64_secret(
                client_id="ec684b8c687f479fadea3cb2ad83f5c6",
                client_secret="e1f31c211f28413186262d37a13fc84d",
            ),
            "ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=",
        )

    def test_get_secret_headers(self):
        client_id = "hello"
        client_secret = "world"
        headers = src.auth_token_utils.get_secret_headers(
            client_id=client_id, client_secret=client_secret
        )
        base64_secret = src.auth_token_utils.convert_to_base64_secret(
            client_id=client_id, client_secret=client_secret
        )
        self.assertIn("Content-Type", headers.keys())
        self.assertEqual(headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertIn("Authorization", headers.keys())
        self.assertEqual(headers["Authorization"], f"basic {base64_secret}")

    def test_get_access_token(self):
        for rely_on_oauth_basic in [False, True]:
            access_token = src.auth_token_utils.get_access_token(
                client_id="hello",
                client_secret="world",
                body_data={"grant_type": "dummy"},
                rely_on_oauth_basic=rely_on_oauth_basic,
                verbose=True,
            )
            self.assertIsNone(access_token)

    def test_get_access_token_with_client_credentials(self):
        access_token = src.auth_token_utils.get_access_token_with_client_credentials(
            client_id="hello", client_secret="world", verbose=True
        )
        self.assertIsNone(access_token)
        # Reference: https://github.com/MixV2/EpicResearch/blob/master/docs/auth/auth_clients.md
        for rely_on_oauth_basic in [False, True]:
            for ask_for_long_token in [False, True]:
                access_token = (
                    src.auth_token_utils.get_access_token_with_client_credentials(
                        client_id="ec684b8c687f479fadea3cb2ad83f5c6",
                        client_secret="e1f31c211f28413186262d37a13fc84d",
                        rely_on_oauth_basic=rely_on_oauth_basic,
                        ask_for_long_token=ask_for_long_token,
                        verbose=True,
                    )
                )
                self.assertIsNotNone(access_token)
                self.assertGreater(len(access_token), 0)
                if ask_for_long_token:
                    expected_access_token_length = 1075
                else:
                    expected_access_token_length = 32
                self.assertEqual(len(access_token), expected_access_token_length)

    def test_get_access_token_with_authorization_code(self):
        for rely_on_oauth_basic in [False, True]:
            for ask_for_long_token in [False, True]:
                access_token = (
                    src.auth_token_utils.get_access_token_with_authorization_code(
                        client_id="hello",
                        client_secret="world",
                        authorization_code="dummy",
                        rely_on_oauth_basic=rely_on_oauth_basic,
                        ask_for_long_token=ask_for_long_token,
                        verbose=True,
                    )
                )
                self.assertIsNone(access_token)

    def test_get_oauth_headers(self):
        headers = src.auth_token_utils.get_oauth_headers(access_token="dummy_token")
        self.assertIn("User-Agent", headers.keys())
        self.assertEqual(
            headers["User-Agent"],
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        )
        self.assertIn("Accept", headers.keys())
        self.assertEqual(headers["Accept"], "application/json")
        self.assertIn("Content-Type", headers.keys())
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertIn("Authorization", headers.keys())
        self.assertEqual(headers["Authorization"], "Bearer dummy_token")


class TestAuthUtils(TestCase):
    def test_get_token(self):
        rely_on_oauth_basic = True
        ask_for_long_token = True
        verbose = True

        target_client_name = "graphqlWebsite"
        client = src.io_utils.load_target_auth_client(
            target_client_name, verbose=verbose
        )

        for authorization_code in ["", "dummy"]:
            access_token = src.auth_utils.get_token(
                client=client,
                authorization_code=authorization_code,
                rely_on_oauth_basic=rely_on_oauth_basic,
                ask_for_long_token=ask_for_long_token,
                verbose=verbose,
            )
            self.assertIsNone(access_token)

        target_client_name = "launcherAppClient2"
        client = src.io_utils.load_target_auth_client(
            target_client_name, verbose=verbose
        )

        authorization_code = ""
        access_token = src.auth_utils.get_token(
            client=client,
            authorization_code=authorization_code,
            rely_on_oauth_basic=rely_on_oauth_basic,
            ask_for_long_token=ask_for_long_token,
            verbose=verbose,
        )
        self.assertGreater(len(access_token), 0)

        authorization_code = "dummy"
        access_token = src.auth_utils.get_token(
            client=client,
            authorization_code=authorization_code,
            rely_on_oauth_basic=rely_on_oauth_basic,
            ask_for_long_token=ask_for_long_token,
            verbose=verbose,
        )
        self.assertIsNone(access_token)

    def test_get_headers(self):
        headers = src.auth_utils.get_headers(access_token=None)
        self.assertNotIn("Authorization", headers.keys())

        headers = src.auth_utils.get_headers(access_token="")
        self.assertNotIn("Authorization", headers.keys())

        dummy_access_token = "dummy"
        expected_headers = src.auth_token_utils.get_oauth_headers(dummy_access_token)

        headers = src.auth_utils.get_headers(dummy_access_token)
        self.assertIn("Authorization", headers.keys())
        self.assertDictEqual(headers, expected_headers)

    def test_get_cookies(self):
        cookies = src.auth_utils.get_cookies(
            authorization_code="hello",
            access_token="world",
            verbose=True,
        )
        self.assertDictEqual(cookies, {"EPIC_BEARER_TOKEN": "world"})
        cookies = src.auth_utils.get_cookies(
            authorization_code="", access_token="world"
        )
        self.assertDictEqual(cookies, {"EPIC_BEARER_TOKEN": "world"})
        cookies = src.auth_utils.get_cookies(
            authorization_code=None, access_token="world"
        )
        self.assertDictEqual(cookies, {"EPIC_BEARER_TOKEN": "world"})
        cookies = src.auth_utils.get_cookies(
            authorization_code="hello",
            access_token="",
            verbose=True,
        )
        self.assertDictEqual(cookies, {"EPIC_BEARER_TOKEN": "hello"})
        cookies = src.auth_utils.get_cookies(
            authorization_code="hello", access_token=None
        )
        self.assertDictEqual(cookies, {"EPIC_BEARER_TOKEN": "hello"})
        cookies = src.auth_utils.get_cookies(
            authorization_code="",
            access_token="",
            verbose=True,
        )
        self.assertEqual(len(cookies), 0)
        cookies = src.auth_utils.get_cookies(authorization_code="", access_token=None)
        self.assertEqual(len(cookies), 0)
        cookies = src.auth_utils.get_cookies(authorization_code=None, access_token="")
        self.assertEqual(len(cookies), 0)
        cookies = src.auth_utils.get_cookies(authorization_code=None, access_token=None)
        self.assertEqual(len(cookies), 0)

    def test_get_simple_json_query(self):
        json_query = src.auth_utils.get_simple_json_query()
        self.assertIn("query", json_query.keys())
        self.assertIn("Catalog", json_query["query"])
        self.assertIn("searchStore(count:3, start: 0)", json_query["query"])
        self.assertIn("{ paging {total} elements {title} }", json_query["query"])

    def test_query_graphql_while_auth(self):
        ask_for_long_token = True
        rely_on_oauth_basic = True
        verbose = True

        target_client_name = "graphqlWebsite"
        authorization_code = ""

        data = src.auth_utils.query_graphql_while_auth(
            target_client_name=target_client_name,
            ask_for_long_token=ask_for_long_token,
            rely_on_oauth_basic=rely_on_oauth_basic,
            authorization_code=authorization_code,
            verbose=verbose,
        )

        self.assertGreaterEqual(len(data), 2)
        self.assertLessEqual(len(data), 3)
        self.assertIn("data", data.keys())
        self.assertIn("extensions", data.keys())
        self.assertEqual(len(data["extensions"]), 0)
        if len(data) > 2:
            self.assertIn("errors", data.keys())
            self.assertGreater(len(data["errors"]), 0)
        self.assertIn("Catalog", data["data"].keys())
        self.assertIn("searchStore", data["data"]["Catalog"].keys())
        # Access to the publicly visible database, with no special permission because the client secret is unknown:
        result = data["data"]["Catalog"]["searchStore"]
        self.assertGreater(len(result), 0)
        self.assertIn("paging", result.keys())
        self.assertIn("total", result["paging"].keys())
        self.assertIn("elements", result.keys())
        self.assertGreater(result["paging"]["total"], 0)
        self.assertGreater(len(result["elements"]), 0)

        target_client_name = "launcherAppClient2"
        authorization_code = ""

        data = src.auth_utils.query_graphql_while_auth(
            target_client_name=target_client_name,
            ask_for_long_token=ask_for_long_token,
            rely_on_oauth_basic=rely_on_oauth_basic,
            authorization_code=authorization_code,
            verbose=verbose,
        )

        self.assertGreaterEqual(len(data), 2)
        self.assertLessEqual(len(data), 3)
        self.assertIn("data", data.keys())
        self.assertIn("extensions", data.keys())
        self.assertEqual(len(data["extensions"]), 0)
        if len(data) > 2:
            self.assertIn("errors", data.keys())
            self.assertGreater(len(data["errors"]), 0)
        self.assertIn("Catalog", data["data"].keys())
        self.assertIn("searchStore", data["data"]["Catalog"].keys())
        # Access token with insufficient permissions when using client credentials:
        result = data["data"]["Catalog"]["searchStore"]
        self.assertIsNone(result)
