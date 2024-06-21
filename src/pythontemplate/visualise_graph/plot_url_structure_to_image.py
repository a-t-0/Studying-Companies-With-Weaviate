from typing import Dict, Optional

import networkx as nx
import pydot
from pydot.core import Dot, Edge
from typeguard import typechecked

from src.pythontemplate.helper import get_output_path


def plot_url_structure_to_svg_pdf_png(
    *,
    graph_dict: Dict,  # type: ignore[type-arg]
    nx_graph: nx.DiGraph,
    graph_plot_filename: str,
    output_dir: str,
    company_url: str,
) -> None:
    """Plots a directed tree given in 2 formats - a dictionary, the
    dictionary's keys represent nodes whose value is another dictionary of
    child nodes which are represented with their corresponding weights.
    Additionally this graph is represented using digraph class of networkx
    which has several methods we're able to use for graph analysis. This
    functions takes as input both dictionary representation of graph along with
    it's networkx-digraph counterpart and.

    creates two different visualizations - png file and svg file using neato
    graph-structure-layout algorithm which tries to draw the graph using
    vertical layering while minimizing number of edge crossings. The
    visualizations are saved into "output.png" for png visualization and
    "output.svg" for svg visualization.

    Args: :graph_dict: (Dict[str, Dict[str, int]]), Dictionary that describes
    the graph - keys represent nodes that are dictionaries with node's weights
    :nx_graph: (nx.DiGraph), Networkx directed graph representing the
    dictionary graph - contains information regarding the nodes of the graph
    and how are
    """
    plot_output_path_without_ext: str = get_output_path(
        output_dir=output_dir,
        company_url=company_url,
        filename=graph_plot_filename,
    )
    graph: Dot = pydot.Dot(graph_type="graph", prog="neato", rankdir="LR")
    visit_node_in_dict(
        nx_graph=nx_graph, graph_dict=graph, node=graph_dict, parent=None
    )
    graph.write_png(f"{plot_output_path_without_ext}.png")
    graph.write_svg(f"{plot_output_path_without_ext}.svg")
    graph.write_pdf(f"{plot_output_path_without_ext}.pdf")


@typechecked
def visit_node_in_dict(
    *,
    nx_graph: nx.DiGraph,
    graph_dict: Dot,
    node: Dict,  # type: ignore[type-arg]
    parent: Optional[str] = None,
) -> None:
    """Recursively visits nodes in a hierarchical structure and visualizes them
    using a Dot graph.

    Args: :nx_graph: (nx.DiGraph), A directed graph used by NetworkX to
    represent the tree structure. :graph_dict: (Dot), A Dot graph used to
    visualize the tree structure. :node: (Dict), A dictionary representing the
    current node in the tree. :parent: (Optional[str]), The name of the parent
    node, used to create connections in the graph. Default is None.
    """

    for (
        key,
        value,
    ) in node.items():
        if isinstance(value, dict):
            # We start with the root node whose parent is None
            # we don't want to graph_dict the None node
            if parent:
                add_edge_to_pydot_graph(
                    graph_dict=graph_dict, parent_name=parent, child_name=key
                )
            visit_node_in_dict(
                nx_graph=nx_graph,
                graph_dict=graph_dict,
                node=value,
                parent=key,
            )
        else:
            if parent is not None:
                add_edge_to_pydot_graph(
                    graph_dict=graph_dict, parent_name=parent, child_name=key
                )
            # drawing the label using a distinct name
            if not isinstance(value, str):
                add_edge_to_pydot_graph(
                    graph_dict=graph_dict,
                    parent_name=key,
                    child_name=key + "_" + value,
                )


@typechecked
def add_edge_to_pydot_graph(
    *,
    graph_dict: Dot,
    parent_name: str,
    child_name: str,
) -> None:
    edge: Edge = pydot.Edge(parent_name, child_name)
    graph_dict.add_edge(edge)
