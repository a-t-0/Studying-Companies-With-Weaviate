// Define a function to populate the dropdown
function populateDropdown() {
	const folderDropdown = document.getElementById("folder-dropdown");
	const selectedFolder = document.createElement("input"); // Create a hidden input for storing the selected folder
	selectedFolder.type = "hidden";
	selectedFolder.name = "selected_folder"; // This name will be accessible in main.js

	// Replace this with your actual logic to get folder names
	const folderNames = getFolderNames("../output_data");

	folderNames.forEach((folderName) => {
		const option = document.createElement("option");
		option.value = folderName;
		option.text = folderName;
		folderDropdown.appendChild(option);
	});

	folderDropdown.addEventListener("change", () => {
		selectedFolder.value = folderDropdown.value;
	});

	document.body.appendChild(selectedFolder); // Add the hidden input to the body
}

// Export the function (optional)
export default populateDropdown;
