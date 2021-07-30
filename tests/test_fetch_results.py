import html
import os
import sys
from unittest import TestCase, main

import orjson
import requests
import responses

RESOLVEIT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
sys.path.append(RESOLVEIT_PATH)

from resolveit.fetch_results import (
    get_link_content,
    get_question_and_answers,
    parse_and_get_results,
)
from resolveit.rparser import Parser
from resolveit.settings import (
    SEARCH_ENDPOINT,
    STACKEXCHANGE_API,
    STACKEXCHANGE_VERSION,
    do_suppress_animation,
)


class TestFetchResults(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        do_suppress_animation()

    @responses.activate
    def test_parse_and_get_results(self) -> None:
        url = f"{STACKEXCHANGE_API}/{STACKEXCHANGE_VERSION}/{SEARCH_ENDPOINT}/"
        stackapi_site_api = "https://api.stackexchange.com/2.2/sites/?pagesize=1000&page=1&filter=%21%2AL1%2AAY-85YllAr2%29"

        with open("tests/fixtures/stackapi.json", "rb") as f:
            stackapi_results = orjson.loads(f.read())["stackapi_results"]
            responses.add(
                responses.GET,
                stackapi_site_api,
                json=stackapi_results,
                status=200,
            )

            responses.add(
                responses.GET,
                url,
                json=stackapi_results,
                status=200,
            )

        expected_result_links = []
        for result in stackapi_results["items"]:
            if result["is_answered"]:
                expected_result_links.append(
                    {
                        "title": html.unescape(result["title"]),
                        "votes": result["score"],
                        "link": result["link"],
                    }
                )

        acutal_result_links = parse_and_get_results("A general query string")
        self.assertEqual(len(acutal_result_links), len(expected_result_links))
        self.assertEqual(acutal_result_links, expected_result_links)

    @responses.activate
    def test_get_link_content(self) -> None:
        url = "https://stackoverflow.com/questions/1085162/commit-only-part-of-a-file-in-git"

        with open("tests/fixtures/stackoverflow.json", "rb") as f:
            stackoverflow_data = orjson.loads(f.read())["html"]
            responses.add(
                responses.GET,
                url,
                body=stackoverflow_data,
                status=200,
            )

        acutal_text = get_link_content(url)
        self.assertEqual(acutal_text, stackoverflow_data)

        responses.reset()

        responses.add(
            responses.GET,
            url,
            body=requests.exceptions.RequestException(),
            status=404,
        )

        self.assertIsNone(get_link_content(url))

        responses.reset()

        responses.add(
            responses.GET,
            url,
            body="",
            status=404,
        )

        # This will check the response.ok condition.
        self.assertIsNone(get_link_content(url))

    @responses.activate
    def test_get_question_and_answers(self) -> None:
        url = "https://stackoverflow.com/questions/1085162/commit-only-part-of-a-file-in-git"

        with open("tests/fixtures/stackoverflow.json", "rb") as f:
            stackoverflow_data = orjson.loads(f.read())["html"]
            responses.add(
                responses.GET,
                url,
                body=stackoverflow_data,
                status=200,
            )

            expected_parsed_data = Parser(stackoverflow_data)

        actual_result = get_question_and_answers(url)

        self.assertEqual(
            actual_result["question"], expected_parsed_data.get_question_data()
        )
        expected_answers_data = expected_parsed_data.get_answers_data()
        self.assertEqual(len(actual_result["answers"]), len(expected_answers_data))
        self.assertListEqual(actual_result["answers"], expected_answers_data)


if __name__ == "__main__":
    main()
