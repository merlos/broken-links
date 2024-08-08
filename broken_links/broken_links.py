import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import fnmatch
import os
import logging

def check_link(url):
    """
    Checks if a given URL is working and redirects to an existing page.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is working and redirects to an existing page, False otherwise.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code in [200]:
            return True
        elif response.status_code in [301, 302]:
            logging.debug(f"Received redirect to {response.headers['Location']}")
            return check_link(response.headers['Location'])
        else:
            logging.debug(f"Received status code {response.status_code} for URL {url}")
            return False
    except requests.RequestException as e:
        logging.debug(f"RequestException for URL {url}: {e}")
        return False

def load_ignore_patterns(ignore_file):
    """
    Loads ignore patterns from a file.

    Args:
        ignore_file (str): The path to the ignore file.

    Returns:
        list: A list of ignore patterns.
    """
    if not os.path.exists(ignore_file):
        return []

    with open(ignore_file, 'r') as file:
        patterns = [line.strip() for line in file if line.strip()]
    return patterns

def should_ignore(url, patterns):
    """
    Checks if a URL should be ignored based on patterns.

    Args:
        url (str): The URL to check.
        patterns (list): A list of ignore patterns.

    Returns:
        bool: True if the URL should be ignored, False otherwise.
    """
    for pattern in patterns:
        if fnmatch.fnmatch(url, pattern):
            return True
    return False

def scrape_links(base_url, only_error, ignore_patterns):
    """
    Scrapes all pages within a URL and checks if the destination links exist.

    Args:
        base_url (str): The base URL to start scraping from.
        only_error (bool): If True, only display errors.
        ignore_patterns (list): A list of ignore patterns.

    Returns:
        None
    """
    pages_analyzed = 0
    links_analyzed = 0
    total_links_working = 0
    total_links_not_working = 0
    external_links_working = 0
    external_links_not_working = 0
    internal_links_working = 0
    internal_links_not_working = 0

    to_visit = [base_url]
    visited = set()

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)
        pages_analyzed += 1

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                anchor_text = link.text.strip()
                logging.debug(f"Found link: {anchor_text}")
                link_url = urljoin(base_url, link['href'])
                links_analyzed += 1

                if should_ignore(link_url, ignore_patterns):
                    if not only_error:
                        logging.info(f"Page: {url}, Anchor: {anchor_text}, Link: {link_url}, Ignored: True")
                    continue

                is_working = check_link(link_url)
                if is_working:
                    total_links_working += 1
                    if urlparse(base_url).netloc == urlparse(link_url).netloc:
                        internal_links_working += 1
                    else:
                        external_links_working += 1
                else:
                    total_links_not_working += 1
                    if urlparse(base_url).netloc == urlparse(link_url).netloc:
                        internal_links_not_working += 1
                    else:
                        external_links_not_working += 1

                if not is_working or not only_error:
                    logging.info(f"Page: {url}, Anchor: {anchor_text}, Link: {link_url}, Working: {is_working}")

                if link_url not in visited and urlparse(base_url).netloc == urlparse(link_url).netloc:
                    to_visit.append(link_url)
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve {url}: {e}")

    logging.info(f"\nSummary:")
    logging.info(f"Pages analyzed: {pages_analyzed}")
    logging.info(f"Links analyzed: {links_analyzed}")
    logging.info(f"Total links working: {total_links_working}")
    logging.info(f"Total links not working: {total_links_not_working}")
    logging.info(f"External links working: {external_links_working}")
    logging.info(f"External links not working: {external_links_not_working}")
    logging.info(f"Internal links working: {internal_links_working}")
    logging.info(f"Internal links not working: {internal_links_not_working}")

    if total_links_not_working > 0:
        exit(1)

