from typing import List

from typeguard import typechecked


@typechecked
def verify_configuration(
    *, company_urls: List[str], json_object_name: str
) -> None:
    """Verifies some requirements on the configuration.

    TODO: verify the skip upload to Weaviate argument is not given if the
    Weaviate database is empty.
    """
    if len(company_urls) < 1:
        raise ValueError("Must specify at least one url.")
    for company_url in company_urls:
        if company_url.endswith("/"):
            raise ValueError(f"Company url:{company_url} cannot end with /")
    if not json_object_name or not json_object_name[0].isupper():
        raise ValueError("String must start with a capitalized letter")
