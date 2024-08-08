import argparse
from .broken_links import scrape_links, load_ignore_patterns

def main():
    parser = argparse.ArgumentParser(description="Scrape a website and check all links.")
    parser.add_argument("url", nargs="?", default="http://localhost:4444/", help="The base URL to start scraping from.")
    parser.add_argument("--only-error", "-o", action="store_true", help="Only display errors.")
    parser.add_argument("--ignore-file", "-i", default="./check-ignore", help="Path to the ignore file.")
    args = parser.parse_args()

    ignore_patterns = load_ignore_patterns(args.ignore_file)
    if args.ignore_file != "./check-ignore" and not ignore_patterns:
        print(f"Ignore file '{args.ignore_file}' does not exist or is empty.")
        exit(1)

    scrape_links(args.url, args.only_error, ignore_patterns)

if __name__ == "__main__":
    main()
