"""Entry point for the project."""

from typing import Dict, List

import networkx as nx

from src.pythontemplate.get_website_data.get_website_data_manager import (
    get_nx_graph_of_website,
)
from src.pythontemplate.visualise_graph.plot_dict import plot_dict_tree
from src.pythontemplate.visualise_graph.visualize_website_tree import (
    export_url_structure_for_d3,
    get_url_dictionary,
)
from src.pythontemplate.weaviate_summaries.manage_weaviate_summaries import (
    ensure_weaviate_summaries_are_available,
)
from src.pythontemplate.weaviate_summaries.summarise_json import (
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
d3_json_output_path: str = "d3_data.json"


def get_website(company_url: str) -> None:
    """Retrieves the website structure of a company.

    Args: :company_url: (str), URL of the company website. Returns: This
    function does not directly return data. Instead, it processes the website
    data and generates various outputs, including:* A summarized website data
    stored in Weaviate* A URL structure dictionary (`url_structure`)* A D3 JSON
    output file for frontend visualization (`d3_json_output_path`)* PDF, SVG,
    and PNG visualizations of the website structure (`graph_dict`)
    """

    website_graph: nx.DiGraph = get_nx_graph_of_website(
        website_data_path=website_data_path,
        company_url=company_url,
        weaviate_local_host_url=weaviate_local_host_url,
        summarised_property=summarised_property,
        json_object_name=json_object_name,
    )

    summarised_data = ensure_weaviate_summaries_are_available(
        summarised_website_data_path=summarised_website_data_path,
        weaviate_local_host_url=weaviate_local_host_url,
        json_object_name=json_object_name,
        summarised_property=summarised_property,
    )

    # Export summaries
    inject_summarisation_into_website_graph(
        data=summarised_data,
        website_graph=website_graph,
        max_nr_of_queries=max_nr_of_queries,
        json_object_name=json_object_name,
        summarised_property=summarised_property,
    )

    url_structure: Dict = get_url_dictionary(  # type: ignore[type-arg]
        G=website_graph, root_url=company_url
    )
    # For frontend.
    export_url_structure_for_d3(
        url_structure=url_structure,
        website_graph=website_graph,
        d3_json_output_path=d3_json_output_path,
    )
    input("Exported frontend data.")
    plot_dict_tree(
        graph_dict={company_url: url_structure}, nx_graph=website_graph
    )
    input("Created pdf, svg and png visualisation of tree.")


for company_url in company_urls:
    get_website(company_url=company_url)
