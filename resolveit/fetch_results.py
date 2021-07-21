import html
from typing import Any, Dict, List, Optional

import requests
from stackapi import StackAPI

from resolveit.rparser import Parser
from resolveit.settings import HEADERS, SEARCH_ENDPOINT


def parse_and_get_results(error_msg: str) -> List[Dict[str, str]]:
    SITE = StackAPI("stackoverflow")
    SITE.max_pages = 1
    SITE.page_size = 50
    results = SITE.fetch(SEARCH_ENDPOINT, sort="votes", order="desc", q=error_msg)
    result_links: List[Dict[str, str]] = []
    for result in results["items"]:
        if result["is_answered"]:
            result_links.append(
                {
                    "title": html.unescape(result["title"]),
                    "votes": result["score"],
                    "link": result["link"],
                }
            )

    return result_links


def get_link_content(link: str) -> Optional[str]:
    """Here we fetch the content text of the link.

    Stackexchange API doesn't provide the full excerpt of any
    questions or answers. Therefore, we need to make a request
    to the provided link to fetch the actual content.
    """
    try:
        response = requests.get(link, headers=HEADERS, timeout=10)
    except requests.exceptions.RequestException:
        return None

    if not response.ok:
        return None

    return response.text


def get_question_and_answers(link: str) -> Dict[str, Any]:
    content = get_link_content(link) or ""
    parsed_data = Parser(content)
    result: Dict[str, Any] = {}
    result["question"] = parsed_data.get_question_data()
    result["answers"] = parsed_data.get_answers_data()
    return result
