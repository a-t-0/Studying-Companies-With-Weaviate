import pydot
from pydot import Node


def draw(graph, parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)


def visit(graph, node, parent=None):
    for (
        k,
        v,
    ) in (
        node.items()
    ):  # If using python3, use node.items() instead of node.iteritems()
        if parent is None:

            graph.add_node(
                Node(
                    # k,
                    "This is the summary placeholder",
                    # URL="This is a summary text.",
                    # shape="box",
                    # comment="CUstomTitle",
                    id="weaviate.io",  # Whats on the text
                    # label="CUstomTitle1",
                    label=k,
                    # peripheries="CUstomTitle2",
                    # group="CUstomTitle3",
                    # target="CUstomTitle4",
                    # z="CUstomTitle5",
                    # texlb="CUstomTitle6",
                    # href="https://google.com",
                )
            )
            input(f"ADDED LABEL:{k}")
        if isinstance(v, dict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if parent:
                draw(graph, parent, k)
            visit(graph, v, k)
        else:
            draw(graph, parent, k)
            # drawing the label using a distinct name
            draw(graph, k, k + "_" + v)


def plot_dict_tree(graph_dict):
    # graph = pydot.Dot(graph_type='graph', rankdir='LR')
    graph = pydot.Dot(graph_type="graph", prog="neato", rankdir="LR")
    # graph = pydot.Dot(graph_type="graph")
    visit(graph, graph_dict)
    # graph.write_png('example1_graph.png',dpi=3000)
    graph.write_png("output.png")
    graph.write_svg(
        "output.svg"
    )  # Replace 'output.svg' with your desired filename
    graph.write_pdf(
        "output.pdf"
    )  # Replace 'output.pdf' with your desired filename
