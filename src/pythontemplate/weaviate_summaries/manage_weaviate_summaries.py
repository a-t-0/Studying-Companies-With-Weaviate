import json
import os
from typing import Dict

from typeguard import typechecked

from src.pythontemplate.get_website_data.website_to_graph import load_from_json
from src.pythontemplate.weaviate_summaries.summarise_json import (
    ask_weaviate_to_summarise,
)


@typechecked
def ensure_weaviate_summaries_are_available(
    summarised_website_data_path: str,
    weaviate_local_host_url: str,
    json_object_name: str,
    summarised_property: str,
) -> Dict:  # type: ignore[type-arg]
    # Perform queries to Weaviate to summarise the data.
    # summarised_data: Union[Dict, None]  # type: ignore[type-arg]
    summarised_data: Dict  # type: ignore[type-arg]
    if not os.path.exists(summarised_website_data_path):
        summarised_data = ask_weaviate_to_summarise(
            weaviate_local_host_url=weaviate_local_host_url,
            json_object_name=json_object_name,
            summarised_property=summarised_property,
        )
        with open(summarised_website_data_path, "w") as f:
            json.dump(
                summarised_data, f, indent=4
            )  # Add indentation for readability

    else:
        summarised_data = load_from_json(filepath=summarised_website_data_path)

    return summarised_data
