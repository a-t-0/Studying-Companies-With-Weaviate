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


def generate_summary(graph, node, level):
    indent = "    " * level
    content = (
        f"{indent}* [{node.replace("/","_")}](./{node.replace("/","_")}.md)\n"
    )
    for child in graph.successors(node):
        content += "".join(generate_summary(graph, child, level + 1))
    return content


def create_markdown_files(graph, node, output_dir):
    file_path = os.path.join(output_dir, f"{node.replace("/","_")}.md")
    print(f"file_path={file_path}")
    with open(file_path, "w") as f:
        f.write(f"# {node.replace("/","_")}\n")
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
        create_markdown_files(graph, child, output_dir)
