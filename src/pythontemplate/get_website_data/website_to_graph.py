"""Example python file with a function."""

import json
import urllib.parse
from typing import Dict

import networkx as nx
import requests
from bs4 import BeautifulSoup
from typeguard import typechecked


@typechecked
def add_weighted_edge(*, graph: nx.DiGraph, source: str, target: str) -> None:
    """Adds an edge to a graph, with a weight that is incremented if the edge
    already exists.

    Args: :graph: (nx.DiGraph), The graph to add the edge to. :source: (str),
    The source node of the edge. :target: (str), The target node of the edge.
    """

    if graph.has_edge(source, target):
        graph[source][target]["weight"] += 1
    else:
        graph.add_edge(source, target, weight=1)


@typechecked
def website_to_graph(
    *,
    root_url: str,
    previous_url: str,
    new_url: str,
    website_graph: nx.DiGraph,
    counter: int,
) -> nx.DiGraph:
    """Crawls a website and its sub URLs, building a directed graph using
    NetworkX. Nodes represent URLs and edges point to child URLs. Each node has
    a 'text_content' attribute to store the extracted text.

    Args:   url: The starting URL of the website.
    """
    print(f"Counter={counter}/?")
    counter += 1
    try:
        response = requests.get(new_url)
        response.raise_for_status()  # Raise exception for non-2xx status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {new_url}: {e}")
        return website_graph

    soup = BeautifulSoup(response.content, "html.parser")

    # Create a graph and add the current URL as a node with text content
    website_graph.add_node(new_url, text_content=get_main_text(url=new_url))

    # Find all links on the page and recursively crawl them
    for link in soup.find_all("a", href=True):
        new_url = urllib.parse.urljoin(root_url, link["href"])

        # Check if link points to the same domain and is not an external link
        if link["href"].startswith("/") and link["href"] != "/":

            # First add the new node and text content, then add edge to new
            # node.
            if new_url not in website_graph.nodes:
                website_to_graph(
                    root_url=root_url,
                    previous_url=new_url,
                    new_url=new_url,
                    website_graph=website_graph,
                    counter=counter,
                )
            add_weighted_edge(
                graph=website_graph, source=previous_url, target=new_url
            )
    return website_graph


@typechecked
def get_main_text(*, url: str) -> str:
    """Extracts the main text from a given URL up to a maximum of 1000
    characters.

    Args: :url: (str), The URL of the webpage to extract the text from.
    Returns: The main text extracted from the webpage, limited to 1000
    characters.
    """
    # Fetch the content of the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract main text (example: getting all the text inside <p> tags)
    main_text = ""
    for p_tag in soup.find_all("p"):
        main_text += p_tag.get_text() + "\n"
    if len(main_text) == 0:
        return ""
    return main_text[: min(len(main_text), 1000)]


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
