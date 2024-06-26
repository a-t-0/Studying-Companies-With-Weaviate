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
from src.pythontemplate.helper import get_output_path


def get_nx_graph_of_website(
    *,
    nx_json_filename: str,
    company_url: str,
    output_dir: str,
) -> nx.DiGraph:
    """Gets the nx.DiGraph of a website, by either downloading the data and
    storing it in the structure, or loading the nx.DiGraph from a json.

    Args: :nx_json_filename: (str), The path to the json file that holds the
    data of the website. :company_url: (str), The company url.
    :weaviate_local_host_url: (str), Weaviate's local host URL.
    :summarised_property: (str), The property which will be used for
    summarization of the output data. :json_object_name: (str), The json object
    name that will hold the output data. Returns: The nx.DiGraph of the
    website.
    """

    # Create Website Graph
    website_graph = nx.DiGraph()

    nx_json_output_path: str = get_output_path(
        output_dir=output_dir,
        company_url=company_url,
        filename=nx_json_filename,
    )
    if not os.path.exists(nx_json_output_path):
        website_to_graph(
            root_url=company_url,
            previous_url=company_url,
            new_url=company_url,
            website_graph=website_graph,
            counter=0,
        )
        graph_to_json(G=website_graph, filepath=nx_json_output_path)
    else:
        website_graph = json_to_graph(filepath=nx_json_output_path)
    # Ensure the json data is loaded into weaviate.

    return website_graph
