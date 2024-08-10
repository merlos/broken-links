from setuptools import setup, find_packages

setup(
    name="broken-links",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "broken-links=broken_links.cli:main",
        ],
    },
    author="merlos",
    author_email="merlos@users.noreply.github.com",
    description="A tool to scrape a website and check for the broken links.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/merlos/broken-links",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
