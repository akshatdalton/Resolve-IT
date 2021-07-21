SEARCH_ENDPOINT = "search/advanced"

VERSION = 1.0

GITHUB_URL = "https://github.com/akshatdalton"

RESOLVE_IT_USER_AGENT = (
    "Mozilla/5.0 (compatible; ResolveIT/{version}; +{external_host})".format(
        version=VERSION, external_host=GITHUB_URL
    )
)

HEADERS = {"User-Agent": RESOLVE_IT_USER_AGENT}

# Following are used only for testing purposes.
STACKEXCHANGE_API = "https://api.stackexchange.com"

STACKEXCHANGE_VERSION = 2.2
