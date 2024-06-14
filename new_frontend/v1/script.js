const treeElement = document.getElementById("navigation-tree");

// Sample tree structure (replace with your actual data)
const treeData = [
  { label: "swag.com", children: [
    { label: "swag.com/fruits", children: [
      { label: "swag.com/fruits/bananas" },
      { label: "swag.com/fruits/oranges" },
    ]},
    // Add more child nodes as needed...
  ]},
];

function buildTree(data, parentElement) {
  for (const item of data) {
    const treeItem = document.createElement("li");
    treeItem.classList.add("tree-item");

    const labelSpan = document.createElement("span");
    labelSpan.textContent = item.label;
    labelSpan.addEventListener("click", () => {
      treeItem.classList.toggle("expanded");
    });

    treeItem.appendChild(labelSpan);

    if (item.children) {
      const childList = document.createElement("ul");
      buildTree(item.children, childList);
      treeItem.appendChild(childList);
    }

    parentElement.appendChild(treeItem);
  }
}

buildTree(treeData, treeElement);

// Handle keyboard navigation (optional)
document.addEventListener("keydown", (event) => {
  const selectedItem = document.activeElement;
  if (selectedItem && selectedItem.tagName === "SPAN") {
    if (event.key === "ArrowUp" && selectedItem.parentElement.previousElementSibling) {
      selectedItem.parentElement.previousElementSibling.querySelector("span").focus();
    } else if (event.key === "ArrowDown" && selectedItem.parentElement.nextElementSibling) {
      selectedItem.parentElement.nextElementSibling.querySelector("span").focus();
    }
  }
});
