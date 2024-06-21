import json
import os
from typing import Dict

from typeguard import typechecked

from src.pythontemplate.get_website_data.nx_graph_json_bridge import (
    load_from_json,
)
from src.pythontemplate.helper import get_output_path
from src.pythontemplate.weaviate_summaries.summarise_json import (
    ask_weaviate_to_summarise,
)


@typechecked
def ensure_weaviate_summaries_are_available(
    summarised_json_filename: str,
    weaviate_local_host_url: str,
    json_object_name: str,
    summarised_property: str,
    output_dir: str,
    company_url: str,
) -> Dict:  # type: ignore[type-arg]

    summarised_json_filepath: str = get_output_path(
        output_dir=output_dir,
        company_url=company_url,
        filename=summarised_json_filename,
    )

    print("Ensuring Weaviate summaries are available.")
    # Perform queries to Weaviate to summarise the data.
    # summarised_data: Union[Dict, None]  # type: ignore[type-arg]
    summarised_data: Dict  # type: ignore[type-arg]
    if not os.path.exists(summarised_json_filepath):
        print("Generating new summaries.")
        summarised_data = ask_weaviate_to_summarise(
            weaviate_local_host_url=weaviate_local_host_url,
            json_object_name=json_object_name,
            summarised_property=summarised_property,
        )
        with open(summarised_json_filepath, "w") as f:
            json.dump(
                summarised_data, f, indent=4
            )  # Add indentation for readability

    else:
        print("Loaded Weaviate summaries from file.")
        summarised_data = load_from_json(filepath=summarised_json_filepath)

    return summarised_data
