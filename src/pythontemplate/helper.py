"""Entry point for the project."""

import os

from typeguard import typechecked


@typechecked
def get_output_path(
    *, output_dir: str, company_url: str, filename: str
) -> str:
    """Returns the output path for the given datafile."""
    url_name: str = strip_leading_https(some_url=company_url)
    if not os.path.exists(f"{output_dir}/{url_name}"):
        raise NotADirectoryError(
            f"Expected output dir:{output_dir}/{url_name} to exist."
        )
    return f"{output_dir}/{url_name}/{filename}"


def strip_leading_https(*, some_url: str) -> str:
    """Removes the leading https:// from an url, if it starts with that."""
    if some_url.startswith("https://"):
        url_name: str = some_url[8:]
    return url_name


@typechecked
def create_output_dir(company_url: str, output_dir: str) -> None:
    """Creates the output directories for the output files."""
    url_name: str = strip_leading_https(some_url=company_url)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if not os.path.exists(output_dir):
        raise NotADirectoryError(f"Expected output dir:{output_dir} to exist.")

    if not os.path.exists(f"{output_dir}/{url_name}"):
        os.mkdir(f"{output_dir}/{url_name}")

    if not os.path.exists(f"{output_dir}/{url_name}"):
        raise NotADirectoryError(
            f"Expected output path:{output_dir}/{url_name} to exist."
        )
