# Broken Links Checker

This tool scrapes all pages within a specified URL and checks if the destination links exist. It reports the original page, the text of the anchor, the destination URL, and whether the link is working or not. If any of the links does not work, the tool exits with an error code. It also provides a summary of the analysis.

It can be run as a **GitHub Action**, as a **command line tool** and as a **Docker Container((.


* [GitHub Action Use](#github-action-use)
* [Command-Line Tool Use](#command-line-tool-use) (pypi)
* [Docker Image Use](#docker-image-use)

## GitHub Action Use

This tool can also be used as a GitHub Action to automatically check links in your repository.

### Inputs
- `url` (optional): The base URL to start scraping from. Default is `http://localhost:4444/`.
- `only-errors` (optional): If set to true, only display errors. Default is `false`.
- `ignore-file` (optional): Path to the ignore file. Default is `./check-ignore`. If the parameter is set and the file does not exist, the action exits with an error. See _Ignore File Format_ section above for more information.

### Ignore File Format

The ignore file should contain one URL pattern per line. The patterns can include wildcards (*) to match multiple URLs. Here are some examples:

- `http://example.com/ignore-this-page` - Ignores this specific URL.
- `http://example.com/ignore/*` - Ignores all URLs that start with `http://example.com/ignore/`.
- `*/ignore-this-path/*` - Ignores all URLs that contain `/ignore-this-path/`.
- `https://*.domain.com*` - Ignores all subdomains of `domain.com` such as `https://sub.domain.com` or `https://sub2.domain.com/page`, etc.


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
        uses: merlos/broken-links@0.2.2
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
        uses: merlos/broken-links@0.2.2
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
        uses: merlos/broken-links@0.2.2
        with:
          url: 'http://localhost:444'
          only-errors: 'true'
          ignore-file: './check-ignore'
```


## Command-Line Tool Use

#### Installation

1. Install the package:
    ```sh
    pip install broken-links
    ```
    
3. Use the `broken-links` command:

  ```sh
  broken-links http://example.com --only-error --ignore-file ./check-ignore
  ```

Command-line arguments:

- `url` (optional): The base URL to start scraping from. Default is `http://localhost:4444/`.
- `--only-error` or `-o` (optional): If set, only display errors. Default is `false`.
- `--ignore-file` or `-i` (optional): Path to the ignore file. Default is `./check-ignore`. If the parameter is NOT set and the file does not exist, it checks all the links. If the parameter is set and the file does not exist, the tool exits with an error. 

The format of the ignore file is explained in the [Ignore File Format (#ignore-file-format) section above.

## Docker Image Use

The docker image has been built for these architectures: `arm64`, `amd64`, and `arm7` and has been released in [docker-hub](https://hub.docker.com/repository/docker/merlos/broken-links/general) and [GitHub Container Registy](https://github.com/merlos/broken-links/pkgs/container/broken-links)


1. Get the image
```sh
docker pull merlos/broken-links:latest
# or from GitHub Container Registry
docker pull ghcr.io/merlos/broken-links:latest
```

2. Run the container
```sh
docker run -ti merlos/broken-links https://www.example.com
```
The arguments are the same as the command line (`url`, `--only-error`, `--ignore-file`) as explained above. The `-ti` option used with `docker` run displays the output of the command as it is generated.  

In order to use the `--ignore-file` argument you need to mount a volume. For example:

```sh
docker run -ti -v /path/on/host/to/ignore-file:/ignore-file merlos/broken-links https://www.example.com --ignore-file /ignore-file
```

## Development

It has been developed using python. So you need to have python installed in your system.

Clone the repository:
```sh
git clone https://github.com/merlos/broken-links
cd broken-links
```

Set a virtual environment:
```sh
python -m venv venv
source venv/bin/activate
```
Install the package in edit mode (`-e`)
```sh
pip install -e .
```
Start coding!

### Build the docker image

```sh
docker build -t broken-links .
```
```sh
docker run --rm broken-links http://example.com --only-error 
```

### Tests
To run the tests, use the following command:

```sh
python -m unittest discover tests
```
## Contributing
Fork and send a pull request. Please update/add the unit tests.

## License
This project is licensed under the terms of the [GNU General Public License v3.0](LICENSE) by merlos.
