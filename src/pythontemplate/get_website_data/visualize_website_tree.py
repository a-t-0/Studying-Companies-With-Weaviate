import networkx as nx
from matplotlib import pyplot as plt
from typeguard import typechecked


@typechecked
def visualize_tree(*, G: nx.digraph, root: int, positions=None):
    """Visualizes a directed graph (G) as a tree starting from the root node.

    Args:
        G: A networkx DiGraph representing the website structure.
        root: The URL of the root node.
        positions: (Optional) A dictionary to pre-define node positions for layout.
    """
    if positions is None:
        positions = nx.nx_agraph.graphviz_layout(G, prog="dot")

    # Subdivide nodes into current level and child levels
    current_level = [root]
    child_levels = {}
    while current_level:
        next_level = []
        for parent in current_level:
            for child in G.successors(parent):
                next_level.append(child)
                if child not in child_levels:
                    child_levels[child] = []
            child_levels[parent] = next_level
        current_level = next_level

    # Draw nodes and edges with hierarchical layout
    nx.draw_networkx_nodes(
        G, positions, nodelist=current_level, node_color="blue"
    )
    for level, nodes in child_levels.items():
        nx.draw_networkx_nodes(
            G, positions, nodelist=nodes, node_color="lightblue"
        )
    nx.draw_networkx_edges(G, positions, alpha=0.7)

    # Label nodes with URLs
    nx.draw_networkx_labels(G, positions, font_size=10)

    plt.axis("off")
    plt.show()



def visualize_tree_v0(tree, root):
    
    safe_graph = nx.DiGraph()
    for node in tree.nodes:
        # TODO; add attributes.
        safe_graph.add_node(check_colon_quotes(s=node))

    # Add edges
    for edge in tree.edges:
        safe_graph.add_edge(check_colon_quotes(s=edge[0]), check_colon_quotes(s=edge[1]))

    pos = graphviz_layout(safe_graph, prog="dot")
    nx.draw(safe_graph, pos)
    plt.show()


    


def check_colon_quotes(s):
    # A quick helper function to check if a string has a colon in it
    # and if it is quoted properly with double quotes.
    # refer https://github.com/pydot/pydot/issues/258
    return ":" in s and (s[0] != '"' or s[-1] != '"')

def visualize_tree_v1(*, G):

    import matplotlib.pyplot as plt
    import networkx as nx
    from networkx.drawing.nx_pydot import graphviz_layout

    # nx.draw_networkx(G, pos = pos, labels = labels, arrows = True,
    nx.draw_networkx(G, arrows = True,
    node_shape = "s", node_color = "white")
    plt.title("Organogram of a company.")
    plt.savefig("eg.jpeg",
    dpi = 300)
    plt.show()