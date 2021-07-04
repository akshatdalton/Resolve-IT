from typing import List

from settings import SEARCH_ENDPOINT
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
