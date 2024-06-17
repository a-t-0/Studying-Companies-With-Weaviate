import os
from typing import List

from typeguard import typechecked


def create_mdbook(graph, root, output_dir: str, summarised_property: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tree: List[List] = []

    tree = create_bft(graph=graph, root_node=list(graph.nodes)[0], tree=tree)

    # Create SUMMARY.md file
    summary_content = ["# Summary\n"]
    summary_content += generate_summary(graph, tree, root)

    with open(os.path.join(output_dir, "SUMMARY.md"), "w") as f:
        f.writelines(summary_content)

    # Create markdown files for each node
    create_markdown_files(
        graph=graph,
        node=root,
        output_dir=output_dir,
        summarised_property=summarised_property,
        visited=None,
    )


def create_bft(graph, root_node, tree: List[List]):
    """Generates a breadth first tree of the graph starting at the root node.

    then adds all its neighbours, then those neighbours etc untill all nodes
    are included in a levelled list.
    """

    if tree == []:
        if root_node is None:
            raise ValueError("Cannot add None as root to tree.")
        tree = [[root_node]]

    # Get the last row of the tree.
    next_level: List = []
    for node in tree[-1]:

        for neighbour in graph.neighbors(node):
            if not tree_contains_node(tree=tree, sought_node=neighbour):
                next_level.append(neighbour)
    if len(next_level) > 0:
        tree.append(next_level)
        for node in tree[-1]:
            tree = create_bft(graph=graph, root_node=root_node, tree=tree)
    return tree


def tree_contains_node(tree: List[List], sought_node) -> bool:
    for nodes_of_level in tree:
        for node in nodes_of_level:
            if sought_node == node:
                return True
    return False


def generate_summary(graph, tree, node):
    """This function generates a summary of a graph structure in Markdown
    format.

    Args:
        graph: A representation of the graph structure.
        node: The current node being processed.
        level: The indentation level for the summary line (increases with depth).
        visited (list, optional): A list to keep track of visited nodes to
        avoid cycles. Defaults to None.

    Returns:
        A string containing the Markdown summary for the current node and its
         descendants.
    """
    content = ""
    for indentation_level, nodes_of_level in enumerate(tree):
        if indentation_level < len(tree) - 1:
            for node in nodes_of_level:
                content += create_summary_content_for_node(
                    level=indentation_level, node=node
                )
                if indentation_level <= len(tree):
                    children = tree[indentation_level + 1]
                    for child in children:
                        if [node, child] in graph.edges:
                            # TODO: include edge weight.
                            content += create_summary_content_for_node(
                                level=indentation_level + 1, node=child
                            )

    return content


def create_summary_content_for_node(*, level: int, node) -> str:
    indent = "    " * level  # Create indentation string based on level
    content = (
        f"{indent}*"
        f" [{node.replace('/', '_')}](./{node.replace('/', '_')}.md)\n"
    )
    return content


@typechecked
def create_markdown_files(
    *, graph, node, output_dir, summarised_property: str, visited=None
):
    """This function creates markdown files for nodes in the graph structure.

    Args:
        graph: A representation of the graph structure.
        node: The current node being processed.
        output_dir: The directory to store the generated markdown files.
        visited (list, optional): A list to keep track of visited nodes to avoid cycles. Defaults to None.
    """
    if visited is None:
        visited = (
            set()
        )  # Initialize visited set for efficiency with membership checks

    if node in visited:
        return  # Skip node if already visited

    visited.add(node)  # Add current node to visited set

    file_path = os.path.join(output_dir, f'{node.replace("/", "_")}.md')
    with open(file_path, "w") as f:
        f.write(f'# {node.replace("/", "_")}\n')
        f.write(graph.nodes[node].get("summary"))

    for child in graph.successors(node):
        create_markdown_files(
            graph=graph,
            node=child,
            output_dir=output_dir,
            summarised_property=summarised_property,
            visited=visited,
        )
