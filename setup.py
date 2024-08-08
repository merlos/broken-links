from setuptools import setup, find_packages

setup(
    name="link_checker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "link-checker=link_checker.cli:main",
        ],
    },
    author="merlos",
    author_email="merlos@users.noreply.github.com",
    description="A tool to scrape a website and check all links.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/merlos/link-checker-action",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
