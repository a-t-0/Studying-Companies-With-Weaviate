"""Entry point for the project."""

import json
import os
from typing import List

import networkx as nx

from src.pythontemplate.frontend.visualise_summarised_website import (
    create_mdbook,
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

# company_urls: List[str] = ["https://weaviate.io"]
# company_urls: List[str] = ["https://thebestmotherfucking.website"]
# company_urls: List[str] = ["https://waarneming.nl/"]
company_urls: List[str] = ["https://trucol.io/"]
website_data_path: str = "website_data.json"
summarised_website_data_path: str = "summarised_by_weaviate.json"
weaveate_local_host_url: str = "http://localhost:8080"
md_book_path: str = "frontend"

# Get the json data.
# website_to_json(urls=company_urls, website_data_path=website_data_path)
# visited = set()  # Initialise an empty website set.
website_graph = nx.DiGraph()  # Initialise an empty website graph.

# website_to_json(
# url=company_urls[0], output_file=website_data_path, visited=visited
# )
if not os.path.exists(website_data_path):
    website_to_graph(
        root_url=company_urls[0],
        previous_url=company_urls[0],
        new_url=company_urls[0],
        website_graph=website_graph,
    )
    graph_to_json(G=website_graph, filepath=website_data_path)

    # visualize_tree(G=website_graph, root=company_urls[0])
    # visualise_tree_v0(tree=website_graph, root=company_urls[0])

    # Limit the number of queries to summarise to 3.
    max_nr_of_queries: int = 3

    # Ensure the json data is loaded into weaviate.
    load_local_json_data_into_weaviate(
        weaveate_local_host_url=weaveate_local_host_url,
        json_input_path=website_data_path,
        json_type="nodes",
        type_property="text_content",
    )
else:
    website_graph = json_to_graph(filepath=website_data_path)

# Perform queries to summarise the data.
if not os.path.exists(summarised_website_data_path):
    summarised_data = ask_weaviate_to_summarise(
        weaveate_local_host_url=weaveate_local_host_url,
        json_type="nodes",
        type_property="text_content",
    )
    with open(summarised_website_data_path, "w") as f:
        json.dump(
            summarised_data, f, indent=4
        )  # Add indentation for readability
else:
    summarised_data = load_from_json(filepath=summarised_website_data_path)

# TODO: add summarized data into the graph.
print(f"summarised_data={summarised_data}")
inject_summarisation_into_website_graph(
    data=summarised_data, website_graph=website_graph
)

# # Example usage
# G = nx.DiGraph()
# G.add_edges_from(
#     [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9)]
# )

# # Add text content to each node
# for i in range(1, 10):
#     G.nodes[i]["text_content"] = f"This is the content for node {i}"
# create_mdbook(graph=G, root=1, output_dir=md_book_path)
# create_mdbook(graph=G, root=1, output_dir=md_book_path)
create_mdbook(
    graph=website_graph, root=company_urls[0], output_dir=md_book_path
)


# Generate plantUML or (md books) website for company.
# generate_summarised_company_website(summarised_data=summarised_data)
