from collections import defaultdict
from typing import List
from urllib.parse import urlparse


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


# Function to convert defaultdict to regular dict
def dictify(d):
    if isinstance(d, defaultdict):
        d = {k: dictify(v) for k, v in d.items()}
    elif isinstance(d, list) and all(isinstance(i, defaultdict) for i in d):
        d = [dictify(i) for i in d]
    return d


def add_url_to_dict(
    full_url: str,
    url_structure: dict,
    url_remainder: str,
    current_path: list[str],
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
        full_url,
        url_structure[new_key],
        remaining_path,
        current_path + [new_key],
    )
