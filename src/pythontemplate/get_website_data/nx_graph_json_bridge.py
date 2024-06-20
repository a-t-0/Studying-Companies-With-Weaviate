"""Example python file with a function."""

import json
from typing import Dict

import networkx as nx
from typeguard import typechecked


@typechecked
def json_to_graph(filepath: str) -> nx.DiGraph:
    """Loads a directed graph from a JSON file generated by `graph_to_json`.

    Args: :filepath: (str), Path to the JSON file containing graph data.
    Returns: A NetworkX DiGraph representing the loaded graph.
    """
    # Read data from the JSON file
    with open(filepath) as f:
        data = json.load(f)

    # Create a directed graph
    G = nx.DiGraph()

    print(f'Got: {len(data["nodes"])} pages.')
    # Add nodes with attributes (if present)
    for node in data["nodes"]:
        # text_content is how networkx stores the node attribute.
        if "text_content" in node.keys():
            page_main_text: str = node["text_content"]

            G.add_node(node["id"], text_content=page_main_text)

    # Add edges
    for edge in data["links"]:
        if edge["source"] in G.nodes and edge["target"] in G.nodes:
            G.add_edge(edge["source"], edge["target"])

    return G


@typechecked
def load_from_json(
    filepath: str,
) -> Dict:  # type: ignore[type-arg]
    """Loads data from a JSON file.

    Args:     filepath: Path to the JSON file.

    Returns:     The loaded data as a Python object.
    """
    with open(filepath) as f:
        data: Dict = json.load(f)  # type: ignore[type-arg]
        return data


@typechecked
def graph_to_json(G: nx.DiGraph, filepath: str) -> None:
    """Exports a NetworkX graph (G) to a JSON file (filepath).

    Args:     G: A NetworkX graph to be exported.     filepath: Path to the
    output JSON file.
    """
    # Use nx.node_link_data to get nodes and edges in JSON format
    data = nx.node_link_data(G)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)  # Add indentation for readability
