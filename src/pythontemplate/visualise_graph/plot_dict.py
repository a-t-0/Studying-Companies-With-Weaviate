from typing import Dict

import networkx as nx
import pydot
from pydot import Node


def draw(graph_dict, parent_name, child_name):
    pydot.Node("hello")
    parent_node = Node(
        "This is the summary placeholder",
        id=parent_name,  # Whats on the text
        label="TheLabel",
    )
    child_node = Node(
        "This is the summary placeholder",
        id=child_name,  # Whats on the text
        label="TheLabel",
    )
    edge = pydot.Edge(parent_name, child_name)
    # print(f'parent_name={parent_name}, childn')
    # edge = pydot.Edge(parent_node, child_node)
    graph_dict.add_edge(edge)


def visit(*, nx_graph: nx.DiGraph, graph_dict, node, parent=None):
    for (
        key,
        value,
    ) in node.items():
        if parent is None:
            print(f"value={value}")
            graph_dict.add_node(
                Node(
                    # value,
                    "This is the summary placeholder",
                    # URL="This is a summary text.",
                    # shape="box",
                    # comment="CUstomTitle",
                    id="weaviate.io",  # Whats on the text
                    # label="CUstomTitle1",
                    label=key,
                    # peripheries="CUstomTitle2",
                    # group="CUstomTitle3",
                    # target="CUstomTitle4",
                    # z="CUstomTitle5",
                    # texlb="CUstomTitle6",
                    # href="https://google.com",
                )
            )
        if isinstance(value, dict):
            # We start with the root node whose parent is None
            # we don't want to graph_dict the None node
            if parent:
                draw(graph_dict, parent, key)
            visit(
                nx_graph=nx_graph,
                graph_dict=graph_dict,
                node=value,
                parent=key,
            )
        else:
            draw(graph_dict, parent, key)
            # drawing the label using a distinct name
            if not isinstance(value, str):
                draw(graph_dict, key, key + "_" + value)
            else:
                # TODO: determine how to set the label of a node without creating an extra node.
                print(
                    f"TODO: get summary from url:{value} and add it as a node"
                    " subtext."
                )
                # the_node=nx_graph.nodes[value]
                print(f'summary={nx_graph.nodes[value]["summary"]}')


def plot_dict_tree(graph_dict: Dict, nx_graph: nx.DiGraph):
    graph = pydot.Dot(graph_type="graph", prog="neato", rankdir="LR")

    visit(nx_graph=nx_graph, graph_dict=graph, node=graph_dict, parent=None)
    graph.write_png("output.png")
    graph.write_svg("output.svg")
    graph.write_pdf("output.pdf")
