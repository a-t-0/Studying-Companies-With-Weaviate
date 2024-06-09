"""Example python file with a function."""

from typeguard import typechecked


@typechecked
def add_two(*, x: int) -> int:
    """Adds a value to an incoming number."""
    return x + 2


import urllib.parse

import requests
from bs4 import BeautifulSoup
from typeguard import typechecked

@typechecked
def website_to_json(*, url:str, output_file:str,visited:set,  indent:int=0, ):
    """Crawls a website and its sub URLs, building a hierarchical tree of URLs
    and their text content.

    Args:
      url: The starting URL of the website.
      indent: Indentation level for the current URL in the tree (internal use).
      output_file: The path to the output text file.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-2xx status codes
    except requests.exceptions.RequestException as e:
        with open(output_file, "a") as f:
            f.write(f"Error fetching {url}: {e}\n")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract text content (replace with your preferred method if needed)
    text_content = soup.get_text(separator="\n").strip()

    # Write URL and content to file
    with open(output_file, "a") as f:
        f.write(" " * indent + url + "\n")
        f.write(" " * (indent + 2) + text_content + "\n\n")

    # Find all links on the page and recursively crawl them
    for link in soup.find_all("a", href=True):
        # Check if link points to the same domain and is not an external link
        if (
            link["href"].startswith("/")
            and link["href"] != "/"
            and urllib.parse.urljoin(url, link["href"]) not in visited
        ):
            visited.add(urllib.parse.urljoin(url, link["href"]))
            website_to_json(
                url = urllib.parse.urljoin(url, link["href"]), output_file=output_file, visited=visited, indent=indent + 2
            )
