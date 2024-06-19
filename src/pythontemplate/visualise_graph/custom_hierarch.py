from typing import Dict
from urllib.parse import urlparse

from typeguard import typechecked


@typechecked
def add_url_to_dict(
    *,
    full_url: str,
    url_structure: Dict,  # type: ignore[type-arg]
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
        full_url=full_url,
        url_structure=url_structure[new_key],
        url_remainder=remaining_path,
        current_path=current_path + [new_key],
    )
