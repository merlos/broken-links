import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
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
            return True, response.status_code
        else:
            logging.debug(f"Received status code {response.status_code} for URL {url}")
            return False, response.status_code
    except requests.RequestException as e:
        logging.debug(f"RequestException for URL {url}: {e}")
        return False, None

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
        # Remove comments. Anything after a '#' is considered a comment.
        patterns = [pattern.split('#')[0].strip() for pattern in patterns]
        # remove empty lines
        patterns = [pattern for pattern in patterns if pattern]
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        logging.debug(f"Loaded ignore patterns: {patterns}")  
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


def remove_anchor(url):
    """
    Removes the anchor (fragment) from a URL.

    Args:
        url (str): The URL to process.

    Returns:
        str: The URL without the anchor.
    """
    parsed_url = urlparse(url)
    # Reconstruct the URL without the fragment
    url_without_anchor = urlunparse(parsed_url._replace(fragment=''))
    return url_without_anchor


def check_if_redirects_to_index(url):
    """
    Checks if a URL redirects to an index file.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL redirects to an index file, False otherwise.
    """
    try:
        response = requests.head(url, allow_redirects=False, timeout=5)
        if response.status_code in [301, 302] and 'Location' in response.headers:
            location = response.headers['Location']
            if location.endswith('/index.html'):
                return True
        return False
    except requests.RequestException as e:
        logging.debug(f"RequestException for URL {url}: {e}")
        return False


def ensure_trailing_slash(url):
    """
    Ensures that any URL that is not a file ends with a '/'.

    Args:
        url (str): The URL to process.

    Returns:
        str: The processed URL with a trailing slash if it's not a file.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Check if the path ends with a file extension
    if not path.endswith('/') and not path.split('/')[-1].count('.'):
        path += '/'

    # Reconstruct the URL with the modified path
    new_url = urlunparse(parsed_url._replace(path=path))
    return new_url


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
    base_path = urlparse(base_url).path
    urls_working_checked = []

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)
        pages_analyzed += 1

        try:
            response = requests.get(url)
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            anchor_text = link.text.strip()
            logging.debug(f"Found link: {anchor_text} -> {link['href']} (current Page: {url})")
            link_url = urljoin(url, link['href'])
            links_analyzed += 1
            if should_ignore(link_url, ignore_patterns):
                if not only_error:
                    logging.info(f"Page: {url}, Anchor: {anchor_text}, Link: {link_url}, Working: Ignored")
                continue
            if link_url in urls_working_checked and not only_error:
                logging.info(f"Skipping link {link_url} as it has already been checked")
                continue
            original_link_url = link_url
            link_url = remove_anchor(link_url)
            is_working, code = check_link(link_url)
            if original_link_url != link_url:
                logging.debug(f"Link {original_link_url} was modified to {link_url}")
            if is_working:
                total_links_working += 1
                urls_working_checked.append(link_url)
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
                logging.info(f"Page: {url}, Anchor: {anchor_text}, Link: {link_url}, Working: {is_working} [{code}]")

            # is the link internal and not in the visited list? -> Add it to the list of links to visit
            if link_url not in visited and urlparse(base_url).netloc == urlparse(link_url).netloc:
                # Ensure that the url starts with the base path, otherwise ignore it. 
                # For example if the base path is /blog/ and the link is /about/ we should ignore it.
                if not link_url.startswith(base_url):
                    logging.debug(f"Skipping appending link {link_url} as it does not start with base URL {base_url}")
                    continue
                logging.debug(f"Adding link {link_url} to visit list")  
                to_visit.append(link_url)
       

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
