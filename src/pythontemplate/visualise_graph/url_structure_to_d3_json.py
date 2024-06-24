import json
from typing import Dict, List

import networkx as nx
from typeguard import typechecked

from src.pythontemplate.helper import get_output_path
from src.pythontemplate.visualise_graph.add_url_to_url_structure_dict import (
    add_url_to_url_structure_dict,
)


@typechecked
def export_url_structure_for_d3(
    url_structure: Dict,  # type: ignore[type-arg]
    website_graph: nx.DiGraph,
    d3_json_filename: str,
    output_dir: str,
    company_url: str,
) -> None:
    """Exports a URL structure in a JSON format suitable for d3 visualization.

    Args: :url_structure: (Dict), A dictionary representing the URL structure
    to export. :website_graph: (nx.DiGraph), A networkx directed graph
    representing the website structure based on which to build the URL
    structure. :d3_json_filename: (str), The path to the output JSON file where
    the exported URL structure will be saved. Returns: The function returns
    None, but the URL structure is exported to a JSON file specified by
    d3_json_filename.
    """

    d3_json_filepath: str = get_output_path(
        output_dir=output_dir,
        company_url=company_url,
        filename=d3_json_filename,
    )
    d3_structure = get_children(
        parent_name=company_url,
        parent_summary="hello",
        parent_url="parent_url",
        url_structure=url_structure,
        website_graph=website_graph,
    )
    with open(d3_json_filepath, "w") as f:
        json.dump(d3_structure, f, indent=4)


@typechecked
def get_children(
    parent_name: str,
    parent_summary: str,
    parent_url: str,
    url_structure: Dict,  # type: ignore[type-arg]
    website_graph: nx.DiGraph,
) -> Dict:  # type: ignore[type-arg]

    if len(list(url_structure.keys())) == 1:
        if isinstance(list(url_structure.values())[0], str):
            # raise ValueError(f"Expected str in:{url_structure}")
            return {
                "name": list(url_structure.keys())[0],
                "summary": website_graph.nodes[
                    list(url_structure.values())[0]
                ]["summary"],
                "url": list(url_structure.values())[0],
            }

    children: List[Dict] = []  # type: ignore[type-arg]
    for key, value in url_structure.items():
        if isinstance(value, str):
            summary = website_graph.nodes[value]["summary"]

            children.append({"name": key, "summary": summary, "url": value})
        elif isinstance(value, dict):
            children.append(
                get_children(
                    parent_name=key,
                    parent_summary="pass",
                    parent_url=parent_url,
                    url_structure=value,
                    website_graph=website_graph,
                )
            )
    return {
        "name": parent_name,
        "summary": parent_summary,
        "url": parent_url,
        "children": children,
    }
    # return d3


@typechecked
def get_url_dictionary(
    *, G: nx.DiGraph, root_url: str
) -> Dict:  # type: ignore[type-arg]
    """Shows nx.digraph as tree structure."""
    url_structure: Dict = {}  # type: ignore[type-arg]

    for url in sorted(G.nodes):
        updated_dict = add_url_to_url_structure_dict(
            full_url=url,
            url_structure=url_structure,
            url_remainder=url,
            current_path=[],
        )
        if updated_dict is not None:
            url_structure = updated_dict
    add_base_url(G=G, url_structure=url_structure, cumulative_url=root_url)
    return url_structure


@typechecked
def add_base_url(
    G: nx.DiGraph,
    url_structure: Dict,  # type: ignore[type-arg]
    cumulative_url: str,
) -> None:
    """Adds the base URL to each empty dictionary at the end of the URL
    structure.

    Args: :G: (nx.DiGraph), The graph containing the pages. :url_structure:
    (Dict), A nested dictionary representing the URL structure.
    :cumulative_url: (str), The cumulative URL of the current dictionary.
    Returns: Modifies the original url_structure in-place.
    """
    #   if url_structure == {}:

    for key, value in url_structure.items():
        if not isinstance(value, dict):
            raise TypeError("Expected dict.")

        if value == {}:
            # Add the base URL if the dictionary is empty
            url_structure[key] = f"{cumulative_url}/{key}"
            if (
                url_structure[key] not in G.nodes
                and f"{url_structure[key]}/" not in G.nodes
            ):
                print(f"G.nodes={G.nodes}")
                print(f"url_structure={url_structure}")
                print(f"key={key}")

                raise ValueError(
                    "The reconstructed url was not found in the nodes."
                )
        else:
            add_base_url(
                G=G,
                url_structure=value,
                cumulative_url=f"{cumulative_url}/{key}",
            )


@typechecked
def make_graph_compliant(G: nx.DiGraph) -> nx.DiGraph:
    plot_graph = nx.DiGraph()
    for node in G.nodes:
        valid_name: str = str(node).replace(":", "_")
        plot_graph.add_node(valid_name)
    for edge in G.edges:
        left = edge[0].replace(":", "_")
        right = edge[1].replace(":", "_")

        # Do not print recurrence.
        if left != right:
            plot_graph.add_edge(left, right)

    return plot_graph


@typechecked
def remove_self_recur(G: nx.DiGraph) -> nx.DiGraph:
    """Removes self recursion in a tree.

    Args: :G: (nx.DiGraph), A tree represented as a directed graph. Returns: A
    tree with self recursion removed.
    """

    removed_edges = []
    for edge in G.edges:
        left = edge[0].replace(":", "_")
        right = edge[1].replace(":", "_")
        # Do not print recurrence.
        if left == right:
            removed_edges.append(edge)

    for removed_edge in removed_edges:
        G.remove_edge(*removed_edge)
    return G
