import re
import logging
from urllib.parse import urlparse

SEARCH_TERM_FILE = "search_terms.txt"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

CATEGORY_RULES = {
    "Educational Resource": {
        "domains": [
            r"\.edu$",
            r"coursera\.org",
            r"khanacademy\.org",
            r"harvard\.edu",
            r"mit\.edu",
        ],
        "keywords": [
            r"\b(tutorial|course|learn|training|syllabus|lecture|study|academy|research)\b"
        ],
    },
    "News Article": {
        "domains": [
            r"bbc\.com",
            r"cnn\.com",
            r"nytimes\.com",
            r"reuters\.com",
            r"forbes\.com",
        ],
        "keywords": [r"\b(news|breaking|report|headlines|latest|journal)\b"],
    },
    "Blog Post": {
        "domains": [
            r"medium\.com",
            r"wordpress\.com",
            r"blogger\.com",
            r"dev\.to",
            r"hashnode\.com",
        ],
        "keywords": [r"\b(blog|opinion|thoughts|insights|guide)\b"],
    },
    "Commercial Site": {
        "domains": [
            r"amazon\.com",
            r"ebay\.com",
            r"shopify\.com",
            r"udemy\.com",
            r"envato\.com",
        ],
        "keywords": [r"\b(sale|discount|buy|pricing|shop|checkout|order now)\b"],
    },
}


def categorize_result(url: str, snippet: str):
    """
    Categorizes a URL based on its domain and snippet content.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower().replace("www.", "")
    snippet_lower = snippet.lower()

    logging.debug(f"Categorizing URL: {url}")
    for category, rules in CATEGORY_RULES.items():
        if any(re.search(pattern, domain) for pattern in rules["domains"]) or any(
            re.search(pattern, snippet_lower) for pattern in rules["keywords"]
        ):
            logging.info(f"Matched category: {category}")
            return category

    logging.info("No match found, categorized as 'Other'")
    return "Other"


def terms_file_parser(path: str = SEARCH_TERM_FILE) -> list:
    """
    Reads search terms from a file and returns them as a list.
    """
    terms = []
    logging.debug(f"Parsing terms from file: {path}")
    with open(path, "r") as f:
        for line in f.readlines():
            terms.append(line.strip())
            logging.debug(f"Term added: {line.strip()}")
    logging.info(f"Parsed {len(terms)} terms from file")
    return terms
