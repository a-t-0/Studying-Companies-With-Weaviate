import networkx as nx
from matplotlib import pyplot as plt

from typeguard import typechecked
from pprint import pprint

import pydot


def draw(graph, parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)
    
def visit(graph, node, parent=None):
    for k,v in node.items():# If using python3, use node.items() instead of node.iteritems()
        if isinstance(v, dict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if parent:
                draw(graph,parent, k)
            visit(graph, v, k)
        else:
            draw(graph,parent, k)
            # drawing the label using a distinct name
            draw(graph, k, k+'_'+v)

def plot_dict_tree(graph_dict):
    graph = pydot.Dot(graph_type='graph')
    visit(graph,graph_dict)
    # graph.write_png('example1_graph.png',dpi=3000)
    graph.write_png('output.png')
    graph.write_svg('output.svg')  # Replace 'output.svg' with your desired filename
    graph.write_pdf('output.pdf')  # Replace 'output.pdf' with your desired filename

