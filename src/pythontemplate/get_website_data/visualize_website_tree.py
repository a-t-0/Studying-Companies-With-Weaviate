import networkx as nx
from matplotlib import pyplot as plt


def visualize_tree(G, root, positions=None):
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


import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


def visualise_tree_v0(tree, root):
    # T = nx.balanced_tree(2, 5)

    # pos = graphviz_layout(T, prog="twopi")
    # for node in tree:
    # print(tree.nodes[node].keys())
    # print(tree.nodes[node]["text_content"])
    # tree.nodes[node]["text_content"]=tree.nodes[node]["text_content"].replace(":", '')
    # node = node.replace(":", "")
    # for node in tree:
    # if ":" in node:
    # raise ValueError("semicolon found in node.")
    # if ":" in tree.nodes[node]["text_content"]:
    # raise ValueError("semicolon found in node text_content.")
    pos = graphviz_layout(tree, prog="dot")
    nx.draw(tree, pos)
    plt.show()


# # Example usage (assuming website_to_graph function exists)
# visited = set()
# G = website_to_graph(url="https://www.example.com", visited=visited)
# root_url = list(G.nodes)[0]  # Assuming unique URLs, get the first node
# visualize_tree(G, root_url)
