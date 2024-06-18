import json
import os

from src.pythontemplate.get_website_data.website_to_graph import load_from_json
from src.pythontemplate.weaviate_summaries.summarise_json import (
    ask_weaviate_to_summarise,
)


def ensure_weaviate_summaries_are_available(
    summarised_website_data_path: str,
    weaviate_local_host_url: str,
    json_object_name: str,
    summarised_property: str,
):
    # Perform queries to Weaviate to summarise the data.
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
