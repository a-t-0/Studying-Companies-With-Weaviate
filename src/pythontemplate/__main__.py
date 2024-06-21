"""Entry point for the project."""

import sys
from typing import Dict, List

import networkx as nx
from typeguard import typechecked

from src.pythontemplate.arg_parsing.arg_parser import parse_skip_upload
from src.pythontemplate.arg_parsing.verify_configuration import (
    verify_configuration,
)
from src.pythontemplate.get_website_data.get_website_data_manager import (
    get_nx_graph_of_website,
)
from src.pythontemplate.load_json_into_weaviate.import_local_json import (
    load_local_json_data_into_weaviate,
)
from src.pythontemplate.visualise_graph.plot_url_structure_to_image import (
    plot_url_structure_to_svg_pdf_png,
)
from src.pythontemplate.visualise_graph.url_structure_to_d3_json import (
    export_url_structure_for_d3,
    get_url_dictionary,
)
from src.pythontemplate.weaviate_summaries.manage_weaviate_summaries import (
    ensure_weaviate_summaries_are_available,
)
from src.pythontemplate.weaviate_summaries.summarise_json import (
    inject_summarisation_into_website_graph,
)

# company_urls: List[str] = ["https://weaviate.io"]
# company_urls: List[str] = ["https://waarneming.nl"]
company_urls: List[str] = ["https://trucol.io"]

website_data_path: str = "website_data.json"
# For this repo the Weaviate data classes are web pages.
json_object_name: str = "WebPage"  # Must start with Capitalised letter.

summarised_property: str = "webPageMainText"
summarised_website_data_path: str = "summarised_by_weaviate.json"
weaviate_local_host_url: str = "http://localhost:8080"

max_nr_of_queries: int = 10000  # Used to prevent timeout error.

d3_json_output_path: str = "d3_data.json"
md_book_path: str = "frontend"

skip_weaviate_upload: bool = parse_skip_upload(
    args=sys.argv[1:]
)  # Skip the script name (sys.argv[0])
verify_configuration(
    company_urls=company_urls, json_object_name=json_object_name
)


@typechecked
def get_summarised_website_tree(
    *, company_url: str, skip_weaviate_upload: bool
) -> None:
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
    )

    if not skip_weaviate_upload:
        load_local_json_data_into_weaviate(
            weaviate_local_host_url=weaviate_local_host_url,
            json_input_path=website_data_path,
            json_object_name=json_object_name,
            summarised_property=summarised_property,
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
    plot_url_structure_to_svg_pdf_png(
        graph_dict={company_url: url_structure}, nx_graph=website_graph
    )
    input("Created pdf, svg and png visualisation of tree.")


for company_url in company_urls:
    get_summarised_website_tree(
        company_url=company_url, skip_weaviate_upload=skip_weaviate_upload
    )
