from stackapi import StackAPI
from pprint import pprint

def parse_and_get_results(error_msg):
    SITE = StackAPI("stackoverflow")
    SITE.max_pages = 1
    results = SITE.fetch("search/advanced", sort="votes", order="desc", q=error_msg)
    result_links = []
    for item in results["items"]:
        if item["is_answered"]:
            result_links.append(item["link"])

    return result_links
