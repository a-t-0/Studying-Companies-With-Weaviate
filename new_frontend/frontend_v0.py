import tkinter as tk


class TreeNode:
    def __init__(self, label, parent=None):
        self.label = label
        self.parent = parent
        self.children = []
        self.expanded = False

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def toggle_expand(self):
        self.expanded = not self.expanded

    def get_label(self):
        return self.label


class TreeView:
    def __init__(self, root_node):
        self.root_node = root_node
        self.window = tk.Tk()
        self.window.title("Website Navigation Tree")
        self.window.bind("<KeyPress>", self.handle_key_press)
        self.current_node = self.root_node
        self.build_tree(self.root_node)
        self.window.mainloop()

    def handle_key_press(self, event):
        if event.keysym == "Up":
            self.go_up()
        elif event.keysym == "Down":
            self.go_down()

    def go_up(self):
        if self.current_node.parent:
            self.current_node = self.current_node.parent
            self.update_tree()

    def go_down(self):
        if self.current_node.expanded and self.current_node.children:
            self.current_node = self.current_node.children[0]
            self.update_tree()

    def update_tree(self):
        self.clear_labels()
        self.build_tree(self.current_node)

    def clear_labels(self):
        for label in self.window.winfo_children():
            if isinstance(label, tk.Label):
                label.destroy()

    def build_tree(self, node, indent=0):
        label = tk.Label(self.window, text="  " * indent + node.get_label())
        label.pack()
        if node == self.current_node and node.expanded:
            for child in node.children:
                self.build_tree(child, indent + 2)


# Example Usage
root_node = TreeNode("swag.com")
root_node.add_child(TreeNode("swag.com/fruits"))
root_node.children[0].add_child(TreeNode("swag.com/fruits/bananas"))
root_node.children[0].add_child(TreeNode("swag.com/fruits/oranges"))
# Add more child nodes as needed...

tree_view = TreeView(root_node)
