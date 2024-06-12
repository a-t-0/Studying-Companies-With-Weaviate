import os


def create_mdbook(graph, root, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create SUMMARY.md file
    summary_content = ["# Summary\n"]
    summary_content += generate_summary(graph, root, 0)

    with open(os.path.join(output_dir, "SUMMARY.md"), "w") as f:
        f.writelines(summary_content)

    # Create markdown files for each node
    create_markdown_files(graph, root, output_dir)

def generate_summary(graph, node, level, visited=None):
    """
    This function generates a summary of a graph structure in Markdown format.

    Args:
        graph: A representation of the graph structure.
        node: The current node being processed.
        level: The indentation level for the summary line (increases with depth).
        visited (list, optional): A list to keep track of visited nodes to avoid cycles. Defaults to None.

    Returns:
        A string containing the Markdown summary for the current node and its descendants.
    """

    indent = "    " * level  # Create indentation string based on level
    content = (
        f'{indent}* [{node.replace("/", "_")}](./{node.replace("/", "_")}.md)\n'
    )

    if visited is None:
        visited = []  # Initialize visited list if not provided

    if node in visited:
        return ""  # Skip node if already visited

    visited.append(node)  # Add current node to visited list

    for child in graph.successors(node):
        """
        Iterate through the successor nodes (children) of the current node.
        """
        content += "".join(generate_summary(graph, child, level + 1, visited))

    return content


# def create_markdown_files(graph, node, output_dir):
    
#     file_path = os.path.join(output_dir, f'{node.replace("/","_")}.md')
#     print(f"file_path={file_path}")
#     with open(file_path, "w") as f:
#         f.write(f'# {node.replace("/","_")}\n')
#         #
#         if "summary" in graph.nodes[node]:
#             f.write(
#                 graph.nodes[node].get(
#                     "text_content", graph.nodes[node]["summary"]
#                 )
#             )
#         else:
#             f.write(graph.nodes[node].get("text_content", "No content"))
#     for child in graph.successors(node):
#         create_markdown_files(graph, child, output_dir)


def create_markdown_files(graph, node, output_dir, visited=None):
  """
  This function creates markdown files for nodes in the graph structure.

  Args:
      graph: A representation of the graph structure.
      node: The current node being processed.
      output_dir: The directory to store the generated markdown files.
      visited (list, optional): A list to keep track of visited nodes to avoid cycles. Defaults to None.
  """
  if visited is None:
    visited = set()  # Initialize visited set for efficiency with membership checks

  if node in visited:
    return  # Skip node if already visited

  visited.add(node)  # Add current node to visited set

  file_path = os.path.join(output_dir, f'{node.replace("/", "_")}.md')
  print(f"file_path={file_path}")
  with open(file_path, "w") as f:
    f.write(f'# {node.replace("/", "_")}\n')
    #
    if "summary" in graph.nodes[node]:
      f.write(
          graph.nodes[node].get(
              "text_content", graph.nodes[node]["summary"]
          )
      )
    else:
      f.write(graph.nodes[node].get("text_content", "No content"))

  for child in graph.successors(node):
    create_markdown_files(graph, child, output_dir, visited)
