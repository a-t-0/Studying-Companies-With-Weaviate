"""Example python file with a function."""

import json
import urllib.parse

import networkx as nx
import requests
from bs4 import BeautifulSoup
from typeguard import typechecked


@typechecked
def website_to_graph(
    *,
    root_url: str,
    previous_url: str,
    new_url: str,
    website_graph: nx.DiGraph,
):
    """Crawls a website and its sub URLs, building a directed graph using
    NetworkX. Nodes represent URLs and edges point to child URLs. Each node has
    a 'text_content' attribute to store the extracted text.

    Args:
      url: The starting URL of the website.
    """
    try:
        response = requests.get(new_url)
        response.raise_for_status()  # Raise exception for non-2xx status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {new_url}: {e}")
        return website_graph

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract text content (replace with your preferred method if needed)
    text_content = soup.get_text(separator="\n").strip()

    # Create a graph and add the current URL as a node with text content
    # website_graph.add_node(new_url.replace(":", ""), text_content=text_content)
    website_graph.add_node(new_url, text_content=get_main_text(url=new_url))
    print(f"website_graph={website_graph}")
    # Find all links on the page and recursively crawl them
    for link in soup.find_all("a", href=True):
        new_url: str = urllib.parse.urljoin(root_url, link["href"])
        # Check if link points to the same domain and is not an external link
        if (
            link["href"].startswith("/")
            and link["href"] != "/"
            and new_url not in website_graph.nodes
        ):
            print(f"new_url={new_url}")
            website_graph.add_edge(previous_url, new_url)
            # website_graph.add_edge(previous_url.replace(":", ""), new_url.replace(":", ""))
            website_to_graph(
                root_url=root_url,
                previous_url=new_url,
                new_url=new_url,
                website_graph=website_graph,
            )
    return website_graph


def get_main_text(*, url: str):
    # Fetch the content of the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract main text (example: getting all the text inside <p> tags)
    main_text = ""
    for p_tag in soup.find_all("p"):
        main_text += p_tag.get_text() + "\n"

    return main_text


def graph_to_json(G: nx.DiGraph, filepath: str):
    """Exports a NetworkX graph (G) to a JSON file (filepath).

    Args:
        G: A NetworkX graph to be exported.
        filepath: Path to the output JSON file.
    """
    # Use nx.node_link_data to get nodes and edges in JSON format
    for node in G.nodes:
        print(f"node={node}")
    data = nx.node_link_data(G)
    # Add additional information if needed (e.g., node attributes)
    counter: int = 0
    # print(f"data={data}")
    # for node, attributes in G.nodes(data=True):

    #     data["nodes"][counter]["text_content"] = attributes.get(
    #         "text_content", None
    #     )
    #     counter += 1
    #     # data.nodes[node]["text_content"] = attributes.get("text_content", None)
    #     input("continu")
    # Write data to JSON file
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)  # Add indentation for readability
