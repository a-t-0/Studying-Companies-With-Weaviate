import urllib.parse

import networkx as nx
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from typeguard import typechecked


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
    print(f"Evaluating url index (non-sorted)={counter}/?")
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
        new_url = get_new_url(root_url=root_url, link=link)
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
def get_new_url(*, root_url: str, link: Tag) -> str:
    """Returning new url from the original url and the beautiful soup link
    dictionary."""
    new_url: str = urllib.parse.urljoin(root_url, link["href"])
    while new_url.endswith("/"):
        new_url = new_url[:-1]  # Remove the trailing slash
    if len(new_url) == 0:
        raise ValueError("Did not find new url.")
    return new_url


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
