import json
from pprint import pprint
from typing import Dict, List

import networkx as nx

from src.pythontemplate.visualise_graph.custom_hierarch import add_url_to_dict


def export_url_structure_for_d3(
    url_structure: Dict, website_graph: nx.DiGraph, d3_json_output_path: str
) -> None:

    # d3_structure:Dict = get_url_structure_for_d3(data=url_structure, website_graph=website_graph)
    # d3_structure: Dict = get_url_structure_for_d3(data=url_structure)
    d3_structure = get_children(
        parent_name="weaviate.io",
        parent_summary="hello",
        parent_url="parent_url",
        url_structure=url_structure,
        website_graph=website_graph,
    )
    pprint(d3_structure)
    with open(d3_json_output_path, "w") as f:
        json.dump(d3_structure, f, indent=4)  # Add indentation for readability


def get_url_structure_for_d3(data):
    """Converts a dictionary to a nested dictionary representing a URL structure.

    Args:
        data: A dictionary containing key-value pairs representing URLs.
            - Top-level keys become child names.
            - Top-level values become child URLs.
            - Nested dictionaries within `data` (if present) are treated as grandchildren.

    Returns:
        A nested dictionary with the following structure:
            {
                "name": "Root",
                "url": "The root url.",  # Replace with your desired root URL description
                "children": [
                    {
                        "name": "Child 1 name",
                        "url": "Child 1 URL",
                        "children": [  # Optional: Grandchildren if nested dictionaries exist
                            ...
                        ]
                    },
                    ...  # More child nodes
                ]
            }
    """

    root_url = (  # Replace with your desired root URL description (optional)
        "The root url."
    )
    children = []
    for name, url in data.items():
        if isinstance(url, str):
            child = {"name": name, "url": url}

        elif isinstance(
            url, dict
        ):  # Check for nested dictionaries (grandchildren)
            grandchildren = []
            grandchildren = get_url_structure_for_d3(url)
            # input(f'url={url}')
            if len(grandchildren) > 0:
                child = {"name": name, "url": "pass"}
                child["children"] = grandchildren
                children.append(child)
    if len(data.keys()) == 1:
        the_name = list(data.keys())[0]
        summary = list(data.values())[0]

        if len(children) > 0:
            return {"name": the_name, "url": summary, "children": children}
        else:
            return {"name": the_name, "url": summary}
    else:
        if len(children) > 0:
            return {
                "name": "rooturl",
                "url": "RootSummary",
                "children": children,
            }
        else:
            return {"name": "rooturl", "url": "RootSummary"}


def get_children(
    parent_name: str,
    parent_summary: str,
    parent_url: str,
    url_structure: Dict,
    website_graph: nx.DiGraph,
) -> None:

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

    children: List[Dict] = []
    for key, value in url_structure.items():
        if isinstance(value, str):
            summary = website_graph.nodes[value]["summary"]
            # print(value)
            # print(summary)

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


def get_url_dictionary(*, G: nx.DiGraph, root_url: str):
    # Source: https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3/29597209#29597209
    """Shows nx.digraph as tree structure."""
    url_structure: dict = {}

    for url in sorted(G.nodes):
        updated_dict = add_url_to_dict(url, url_structure, url, [])
        if updated_dict != None:
            url_structure = updated_dict
    add_base_url(G=G, url_structure=url_structure, cumulative_url=root_url)
    pprint(url_structure)
    input("COntinue?")
    return url_structure


def add_base_url(G: nx.DiGraph, url_structure, cumulative_url: str):
    """
    Adds the base URL to each empty dictionary at the end of the URL structure.

    Args:
      url_structure: A nested dictionary representing the URL structure.
      base_url: The base URL to be added.

    Modifies the original url_structure in-place.
    """
    #   if url_structure == {}:
    for key, value in url_structure.items():
        if not isinstance(value, dict):
            raise TypeError("Expected dict.")

        if value == {}:
            # Add the base URL if the dictionary is empty
            url_structure[key] = f"{cumulative_url}/{key}"
            if url_structure[key] not in G.nodes:
                raise ValueError(
                    "The reconstructed url was not found in the nodes."
                )
        else:
            add_base_url(
                G=G,
                url_structure=value,
                cumulative_url=f"{cumulative_url}/{key}",
            )


def make_graph_compliant(G):
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


def remove_self_recur(G):

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
