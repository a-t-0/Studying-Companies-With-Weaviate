from collections import defaultdict
from typing import List


class WebsiteHierarchy:
    """
    This class represents a website's hierarchical structure and can ingest arbitrary URLs.
    """

    def __init__(self):
        self.hierarchy = defaultdict(
            WebsiteHierarchy
        )  # Nested dictionaries for hierarchy

    def add_url(self, url):
        """
        This function adds a URL to the website hierarchy.

        Args:
            url: A string containing the URL.

        Raises:
            ValueError: If the URL is invalid or has a fragment identifier (#).
        """
        # if "#" in url:
        #   raise ValueError("URLs with fragment identifiers (#) are not supported.")
        domain, *path_components = url.split("/", 3)
        # Handle invalid URLs (e.g., missing domain or empty path)
        if not domain or not path_components:
            return  # Silently ignore invalid URLs

        # Recursively add sub-paths
        self.hierarchy[path_components[0]].add_url(
            "/".join(path_components[1:])
        )

    def get_hierarchy(self):
        """
        This function returns the website hierarchy dictionary.

        Returns:
            A dictionary representing the website's hierarchy.
        """
        # Return a copy to avoid modifying the internal structure
        return dict(self.hierarchy)


def build_hierarchy_v0(urls: List[str]):
    """
    This function takes a list of URLs and builds a dictionary representing
    the website's hierarchical structure.

    Args:
        urls: A list of strings containing URLs.

    Returns:
        A dictionary representing the website's hierarchy.
    """
    hierarchy = defaultdict(list)
    current_path = []
    for url in urls:
        # Extract domain and path components
        domain, *path_components = url.split("/", 3)

        # Update current path based on path depth
        current_path = current_path[: len(path_components)] + path_components

        # Add the last component (excluding domain) to the current level
        if len(current_path) > 1:
            hierarchy[current_path[-2]].append(current_path[-1])

    return {
        "weaviate.io": hierarchy
    }  # Assuming "weaviate.io" is the root domain


def build_hierarchy(urls: List[str], root: str, hierarchy=None, path=[]):
    """
    This function recursively builds a dictionary representing the website's
    hierarchical structure.

    Args:
        url: A string containing the URL.
        hierarchy: A dictionary to store the hierarchy (optional, used internally).
        path: A list representing the current path components (optional, used internally).

    Returns:
        A dictionary representing the website's hierarchy.
    """
    if hierarchy is None:
        hierarchy = defaultdict(list)
    domain, *path_components = url.split("/", 3)

    if not path_components:
        return hierarchy  # Base case: Reached the root domain

    # Update path
    current_path = path + [path_components[0]]

    # Recursive call for sub-paths
    hierarchy[current_path[0]] = build_hierarchy(
        "/".join(path_components), hierarchy.copy(), current_path
    )

    # No need to add anything to the current level as recursion handles it

    return hierarchy


from collections import defaultdict
from urllib.parse import urlparse


def unpack_urls(urls):
    def nested_dict():
        return defaultdict(nested_dict)

    def insert(d, keys, value):
        for key in keys[:-1]:
            d = d[key]

        if keys:
            d[keys[-1]]: value

    hierarchy = nested_dict()

    for url in urls:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path_parts = parsed_url.path.strip("/").split("/")

        if not path_parts:
            continue

        # Insert into hierarchy
        insert(hierarchy[domain], path_parts[:-1], path_parts[-1])

    return hierarchy


# Function to convert defaultdict to regular dict
def dictify(d):
    if isinstance(d, defaultdict):
        d = {k: dictify(v) for k, v in d.items()}
    elif isinstance(d, list) and all(isinstance(i, defaultdict) for i in d):
        d = [dictify(i) for i in d]
    return d


def add_url_to_dict(
    url_structure: dict, url_remainder: str, current_path: list[str]
) -> None:
    parsed_url = urlparse(url_remainder)
    path_parts = parsed_url.path.strip("/").split("/")

    if len(path_parts) == 0 or (path_parts[0] == "" and len(path_parts) == 1):
        return  # Handle empty paths

    new_key = path_parts[0]
    remaining_path = "/".join(path_parts[1:])

    # Check if key already exists, create sub-dictionary if needed
    if new_key not in url_structure:
        url_structure[new_key] = {}

    # Recursive call with updated current_path and remaining path
    add_url_to_dict(
        url_structure[new_key], remaining_path, current_path + [new_key]
    )


def add_nested_dict_entry(
    some_dict: dict, current_path: list[str], new_key: str, new_value
):
    d = some_dict
    for key in current_path:
        if key not in d:
            d[key] = {}
        d = d[key]
    d[new_key] = new_value
