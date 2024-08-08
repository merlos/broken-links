# Broken links Checker GitHub Action && command line tool

This tool scrapes all pages within a specified URL and checks if the destination links exist. It reports the original page, the text of the anchor, the destination URL, and whether the link is working or not. If any link does not work, the tool exits with an error code. It also provides a summary of the analysis.

It can be run as a GitHub Action or as a command line tool.

# Usage

### Command-Line Utility

#### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/merlos/broken-links.git
   cd broken-links
   ````

2. Install the package:

    ```
    pip install .
    ```

3. Use the `broken-links` command to run the script:

```
broken-links http://example.com --only-error --ignore-file ./check-ignore
```

Command-line arguments:

- `url` (optional): The base URL to start scraping from. Default is `http://localhost:4444/`.
- `--only-error` or `-o` (optional): If set, only display errors. Default is `false`.
- `--ignore-file` or `-i` (optional): Path to the ignore file. Default is `./check-ignore`. If the parameter is NOT set and the file does not exist, it checks all the links. If the parameter is set and the file does not exist, the tool exits with an error. 

### Ignore File Format

The ignore file should contain one URL pattern per line. The patterns can include wildcards (*) to match multiple URLs. Here are some examples:

- `http://example.com/ignore-this-page` - Ignores this specific URL.
- `http://example.com/ignore/*` - Ignores all URLs that start with `http://example.com/ignore/`.
- `*/ignore-this-path/*` - Ignores all URLs that contain `/ignore-this-path/`.
- `https://*.domain.com*` - Ignores all subdomains of `domain.com` such as `https://sub.domain.com` or `https://sub2.domain.com/page`, etc.


## GitHub Action

This tool can also be used as a GitHub Action to automatically check links in your repository.

### Inputs
- `url` (optional): The base URL to start scraping from. Default is `http://localhost:4444/`.
- `only-errors` (optional): If set to true, only display errors. Default is `false`.
- `ignore-file` (optional): Path to the ignore file. Default is `./check-ignore`. If the parameter is set and the file does not exist, the action exits with an error. See _Ignore File Format_ section above for more information.

### Outputs

This action does not produce any outputs. However, at the end of the analysis, it prints a summary of the results with:

- Number of pages analyzed
- Number of links analyzed
- Total number of links working
- Total number of links not working
- Number of external links working
- Number of external links not working
- Number of internal links working
- Number of internal links not working

### Examples of Usage

#### Basic Usage (external URL)

```yaml
name: Broken-links Checker

on: [push]

jobs:
  check-links:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Run Link Checker
        uses: ./
        with:
          url: 'http://example.com'
          only-errors: 'true'
```

#### Check links with MkDocs

```yaml
name: MkDocs Preview and Link Check

on:
  push:
    branches:
      - main

jobs:
  preview_and_check:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs mkdocs-material

      - name: Run MkDocs server
        run: mkdocs serve -a 0.0.0.0:4444 &
        continue-on-error: true

      - name: Wait for server to start
        run: sleep 10

      - name: Run Link Checker
        uses: ./
        with:
          url: 'http://localhost:4444'
          only-errors: 'true'
          ignore-file: './check-ignore'
```

#### Check links with Quarto

```yaml
name: Quarto Preview and Link Check

on:
  push:
    branches:
      - main

jobs:
  preview_and_check:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Quarto
        uses: quarto-dev/quarto-actions/setup@v2

      - name: Render Quarto project
        run: quarto preview --port 444 &
        continue-on-error: true

      - name: Wait for server to start
        run: sleep 10

      - name: Run Link Checker
        uses: ./
        with:
          url: 'http://localhost:444'
          only-errors: 'true'
          ignore-file: './check-ignore'
```


## Development

Clone the repository:
```sh
git clone https://github.com/merlos/broken-links
cd broken-links
```
Start coding!

### Build the docker image

```sh
docker build -t broken-links .
```
```sh
docker run --rm broken-links http://example.com --only-error --ignore-file ./check-ignore
```

### Tests
To run the tests, use the following command:

```sh
python -m unittest discover tests
```


## License
This project is licensed under the terms of the [GNU General Public License v3.0](LICENSE) by merlos.