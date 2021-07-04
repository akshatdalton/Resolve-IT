from typing import List, Optional

import requests
from settings import HEADERS, SEARCH_ENDPOINT
from stackapi import StackAPI


def parse_and_get_results(error_msg: str) -> List[str]:
    SITE = StackAPI("stackoverflow")
    SITE.max_pages = 1
    results = SITE.fetch(SEARCH_ENDPOINT, sort="votes", order="desc", q=error_msg)
    result_links: List[str] = []
    for item in results["items"]:
        if item["is_answered"]:
            result_links.append(item["link"])

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
