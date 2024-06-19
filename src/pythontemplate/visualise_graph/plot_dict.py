from typing import Dict, Optional

import networkx as nx
import pydot
from pydot.core import Dot, Edge
from typeguard import typechecked


@typechecked
def draw(
    *,
    graph_dict: Dot,
    parent_name: str,
    child_name: str,
) -> None:
    edge: Edge = pydot.Edge(parent_name, child_name)
    graph_dict.add_edge(edge)


@typechecked
def visit(
    *,
    nx_graph: nx.DiGraph,
    graph_dict: Dot,
    node: Dict,  # type: ignore[type-arg]
    parent: Optional[str] = None,
) -> None:
    for (
        key,
        value,
    ) in node.items():
        if isinstance(value, dict):
            # We start with the root node whose parent is None
            # we don't want to graph_dict the None node
            if parent:
                draw(graph_dict=graph_dict, parent_name=parent, child_name=key)
            visit(
                nx_graph=nx_graph,
                graph_dict=graph_dict,
                node=value,
                parent=key,
            )
        else:
            if parent is not None:
                draw(graph_dict=graph_dict, parent_name=parent, child_name=key)
            # drawing the label using a distinct name
            if not isinstance(value, str):
                draw(
                    graph_dict=graph_dict,
                    parent_name=key,
                    child_name=key + "_" + value,
                )


def plot_dict_tree(
    *, graph_dict: Dict, nx_graph: nx.DiGraph  # type: ignore[type-arg]
) -> None:
    graph: Dot = pydot.Dot(graph_type="graph", prog="neato", rankdir="LR")
    visit(nx_graph=nx_graph, graph_dict=graph, node=graph_dict, parent=None)
    graph.write_png("output.png")
    graph.write_svg("output.svg")
    graph.write_pdf("output.pdf")
