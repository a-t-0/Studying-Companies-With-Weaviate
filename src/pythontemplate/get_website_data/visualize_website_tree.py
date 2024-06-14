import networkx as nx
from matplotlib import pyplot as plt
from src.pythontemplate.get_website_data.custom_hierarch import WebsiteHierarchy, add_url_to_dict, build_hierarchy, dictify, unpack_urls
from src.pythontemplate.get_website_data.plot_dict import plot_dict_tree
from typeguard import typechecked
from pprint import pprint
from src.pythontemplate.get_website_data.hierarchy_evenly_spaced import (
    hierarchy_pos_evenly_spaced,
)
from src.pythontemplate.get_website_data.hierarchy_no_recur import (
    hierarchy_pos_no_recur,
)


@typechecked
def visualize_tree_v1(*, G: nx.DiGraph):
    """Shows nx.digraph as tree structure."""
    # nx.draw_networkx(G, pos = pos, labels = labels, arrows = True,
    nx.draw_networkx(G, arrows=True, node_shape="s", node_color="white")
    # plt.title("Organogram of a company.")
    plt.savefig("eg.jpeg", dpi=300)
    plt.show()


import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


def visualize_tree_v2(*, G: nx.DiGraph):
    # Source: https://stackoverflow.com/questions/57512155/how-to-draw-a-tree-more-beautifully-in-networkx
    plot_graph = make_graph_compliant(G=G)
    # pos = graphviz_layout(plot_graph, prog="twopi")
    pos = graphviz_layout(plot_graph, prog="dot")
    nx.draw(plot_graph, pos)
    plt.show()


def make_graph_compliant(G):
    plot_graph = nx.DiGraph()
    for node in G.nodes:
        valid_name: str = str(node).replace(":", "_")
        plot_graph.add_node(valid_name)
    for edge in G.edges:
        left = edge[0].replace(":", "_")
        right = edge[1].replace(":", "_")
        
        # Do not print recurrence.
        if left != right:
            plot_graph.add_edge(left, right)


    return plot_graph

def remove_self_recur(G):
    
    removed_edges=[]
    for edge in G.edges:
        left = edge[0].replace(":", "_")
        right = edge[1].replace(":", "_")
        # Do not print recurrence.
        if left == right:
            removed_edges.append(edge)
        
    for removed_edge in removed_edges:
        G.remove_edge(*removed_edge)
    return G



def visualize_tree_v3(*, G: nx.DiGraph, root: str):
    """Shows nx.digraph as tree structure."""
    # nx.draw_networkx(G, pos = pos, labels = labels, arrows = True,
    nx.draw_networkx(G, arrows=True, node_shape="s", node_color="white")
    pos = hierarchy_pos_evenly_spaced(G=G, root=root)
    print("Got hierarchy")
    nx.draw(G, pos=pos, with_labels=True)
    plt.savefig("hierarchy.png")


def visualize_tree_v4(*, G: nx.DiGraph):
    """Shows nx.digraph as tree structure."""
    plot_graph = make_graph_compliant(G=G)
    p = nx.drawing.nx_pydot.to_pydot(plot_graph)
    p.write_png("example.png")


def visualize_tree_v5(*, G: nx.DiGraph, root: str):
    # Source: https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3/29597209#29597209
    """Shows nx.digraph as tree structure."""
    # hierarchy=build_hierarchy(G.nodes)
    # pprint(hierarchy)
    # website_hierarchy = WebsiteHierarchy()
    url_structure: dict={}

    for url in G.nodes:
        print(url)
        updated_dict = add_url_to_dict(url_structure, url,[])
        if updated_dict != None:
            url_structure =updated_dict
    print("done")
    
    plot_dict_tree(graph_dict={"weaviate.io":url_structure})
    