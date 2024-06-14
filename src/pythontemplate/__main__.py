"""Entry point for the project."""

import json
import os
from typing import List

import networkx as nx

from src.pythontemplate.frontend.visualize_summarised_website import (
    create_mdbook,
)
from src.pythontemplate.get_website_data.visualize_website_tree import (
    visualize_tree_v5,
)
from src.pythontemplate.get_website_data.website_to_graph import (
    graph_to_json,
    json_to_graph,
    load_from_json,
    website_to_graph,
)
from src.pythontemplate.load_json_into_weaviate.import_local_json import (
    load_local_json_data_into_weaviate,
)
from src.pythontemplate.summarise_json import (
    ask_weaviate_to_summarise,
    inject_summarisation_into_website_graph,
)

company_urls: List[str] = ["https://weaviate.io"]
# company_urls: List[str] = ["https://waarneming.nl/"]
# company_urls: List[str] = ["https://trucol.io/"]
website_data_path: str = "website_data.json"
# For this repo the Weaviate data classes are web pages.
json_object_name: str = "WebPage"  # Must start with Capitalised letter.
# For this repo, the Weaviate property that is being summarised by is the
# main text of the web page.
summarised_property: str = "webPageMainText"
summarised_website_data_path: str = "summarised_by_weaviate.json"
weaviate_local_host_url: str = "http://localhost:8080"
md_book_path: str = "frontend"
max_nr_of_queries: int = 10000  # Used to prevent timeout error.

website_graph = nx.DiGraph()
if not os.path.exists(website_data_path):
    website_to_graph(
        root_url=company_urls[0],
        previous_url=company_urls[0],
        new_url=company_urls[0],
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
    website_graph = json_to_graph(
        filepath=website_data_path, summarised_property=summarised_property
    )
print("Start visual")
# visualize_tree_v2(G=website_graph)
# visualize_tree_v3(G=website_graph, root=company_urls[0])
# visualize_tree_v4(G=website_graph)
visualize_tree_v5(G=website_graph, root=company_urls[0])
input("ENDED visual")

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

inject_summarisation_into_website_graph(
    data=summarised_data,
    website_graph=website_graph,
    max_nr_of_queries=max_nr_of_queries,
    json_object_name=json_object_name,
    summarised_property=summarised_property,
)

# visualize_tree_v1(G=website_graph)


create_mdbook(
    graph=website_graph,
    root=company_urls[0],
    output_dir=md_book_path,
    summarised_property=summarised_property,
)
