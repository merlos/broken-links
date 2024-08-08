# Link Checker GitHub Action

This GitHub Action scrapes all pages within a specified URL and checks if the destination links exist. It reports the original page, the text of the anchor, the destination URL, and whether the link is working or not. If any link does not work, the action exits with an error code. It also provides a summary of the analysis.

## Inputs

### `url`

**Optional** The base URL to start scraping from. Default is `http://localhost:4444/`.

### `only-errors`

**Optional** If set to `true`, only display errors. Default is `false`.

## Outputs

This action does not produce any outputs. However, at the end of the analysis, it prints a summary of the results with: 

* Number of pages analyzed
* Number of links analyzed
* Total number of links working
* Total number of links not working
* Number of external links working
* Number of external links not working
* Number of internal links working
* Number of internal links not working

## Examples of Usage

### Basic Usage (external URL)
```yaml
name: Link Checker

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

### Check links with quarto 

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
        run: quarto preview --port 4444 &
        continue-on-error: true

      - name: Wait for server to start
        run: sleep 10

      - name: Run Link Checker
        uses: ./
        with:
          url: 'http://localhost:4444'
          only-errors: 'true'
```

### Check links with MKDocs

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
```

## License
This project is licensed under the terms of the GNU [General Public License v3.0](LICENSE) by merlos