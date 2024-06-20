"""Example python file with a function."""

import os

import networkx as nx

from src.pythontemplate.get_website_data.nx_graph_json_bridge import (
    graph_to_json,
    json_to_graph,
)
from src.pythontemplate.get_website_data.website_to_graph import (
    website_to_graph,
)
from src.pythontemplate.load_json_into_weaviate.import_local_json import (
    load_local_json_data_into_weaviate,
)


def get_nx_graph_of_website(
    *,
    website_data_path: str,
    company_url: str,
    weaviate_local_host_url: str,
    summarised_property: str,
    json_object_name: str,
) -> nx.DiGraph:
    """Gets the nx.DiGraph of a website, by either downloading the data and
    storing it in the structure, or loading the nx.DiGraph from a json.

    Args: :website_data_path: (str), The path to the json file that holds the
    data of the website. :company_url: (str), The company url.
    :weaviate_local_host_url: (str), Weaviate's local host URL.
    :summarised_property: (str), The property which will be used for
    summarization of the output data. :json_object_name: (str), The json object
    name that will hold the output data. Returns: The nx.DiGraph of the
    website.
    """

    # Create Website Graph
    website_graph = nx.DiGraph()
    if not os.path.exists(website_data_path):
        website_to_graph(
            root_url=company_url,
            previous_url=company_url,
            new_url=company_url,
            website_graph=website_graph,
            counter=0,
        )
        graph_to_json(G=website_graph, filepath=website_data_path)

        # Ensure the json data is loaded into weaviate.
        load_local_json_data_into_weaviate(
            weaviate_local_host_url=weaviate_local_host_url,
            json_input_path=website_data_path,
            json_object_name=json_object_name,
            summarised_property=summarised_property,
        )

    else:
        website_graph = json_to_graph(filepath=website_data_path)
    return website_graph
