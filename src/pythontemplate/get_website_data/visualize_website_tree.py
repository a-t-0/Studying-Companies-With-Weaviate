import networkx as nx
from matplotlib import pyplot as plt
from typeguard import typechecked


@typechecked
def visualize_tree_v1(*, G: nx.DiGraph):
    """Shows nx.digraph as tree structure."""
    # nx.draw_networkx(G, pos = pos, labels = labels, arrows = True,
    nx.draw_networkx(G, arrows=True, node_shape="s", node_color="white")
    plt.title("Organogram of a company.")
    plt.savefig("eg.jpeg", dpi=300)
    plt.show()
