

document.addEventListener("DOMContentLoaded", function() {
    let container = document.getElementById('container');

    // Copyright 2021-2023 Observable, Inc.
    // Released under the ISC license.
    // https://observablehq.com/@d3/tree
    function Tree(data, { // data is either tabular (array of objects) or hierarchy (nested objects)
        path, // as an alternative to id and parentId, returns an array identifier, imputing internal nodes
        id = Array.isArray(data) ? d => d.id : null, // if tabular data, given a d in data, returns a unique identifier (string)
        parentId = Array.isArray(data) ? d => d.parentId : null, // if tabular data, given a node d, returns its parent’s identifier
        children, // if hierarchical data, given a d in data, returns its children
        tree = d3.tree, // layout algorithm (typically d3.tree or d3.cluster)
        sort, // how to sort nodes prior to layout (e.g., (a, b) => d3.descending(a.height, b.height))
        label, // given a node d, returns the display name
        title, // given a node d, returns its hover text
        link, // given a node d, its link (if any)
        linkTarget = "_blank", // the target attribute for links (if any)
        width = 1600, // outer width, in pixels
        height, // outer height, in pixels
        r = 4, // radius of nodes
        padding = 1, // horizontal padding for first and last column (Larger is smaller padding)
        fill = "#999", // fill for nodes
        fillOpacity, // fill opacity for nodes
        stroke = "#555", // stroke for links
        strokeWidth = 1.5, // stroke width for links
        strokeOpacity = 0.4, // stroke opacity for links
        strokeLinejoin, // stroke line join for links
        strokeLinecap, // stroke line cap for links
        halo = "#fff", // color of label halo
        haloWidth = 3, // padding around the labels
        curve = d3.curveBumpX, // curve for the link
      } = {}) {

        // If id and parentId options are specified, or the path option, use d3.stratify
        // to convert tabular data to a hierarchy; otherwise we assume that the data is
        // specified as an object {children} with nested objects (a.k.a. the “flare.json”
        // format), and use d3.hierarchy.
        const root = path != null ? d3.stratify().path(path)(data)
            : id != null || parentId != null ? d3.stratify().id(id).parentId(parentId)(data)
            : d3.hierarchy(data, children);

        // Sort the nodes.
        if (sort != null) root.sort(sort);

        // Compute labels and titles.
        const descendants = root.descendants();
        const L = label == null ? null : descendants.map(d => label(d.data, d));

        // Compute the layout.
        const dx = 12; // The dx is the vertical spacing
        const dy =15+ width / (root.height + padding); // The dy is the horizontal spacing.
        tree().nodeSize([dx, dy])(root);

        // Center the tree.
        let x0 = Infinity;
        let x1 = -x0;
        root.each(d => {
          if (d.x > x1) x1 = d.x;
          if (d.x < x0) x0 = d.x;
        });

        // Compute the default height.
        if (height === undefined) height = x1 - x0 + dx * 2;

        // Use the required curve
        if (typeof curve !== "function") throw new Error(`Unsupported curve`);


        const svg = d3.create("svg")
            .attr("viewBox", [-dy * padding / 2, x0 - dx, width, height])
            .attr("width", width)
            .attr("height", height)
            .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
            .attr("font-family", "sans-serif")
            .attr("font-size", 10);

        svg.append("g")
            .attr("fill", "none")
            .attr("stroke", stroke)
            .attr("stroke-opacity", strokeOpacity)
            .attr("stroke-linecap", strokeLinecap)
            .attr("stroke-linejoin", strokeLinejoin)
            .attr("stroke-width", strokeWidth)
          .selectAll("path")
            .data(root.links())
            .join("path")
              .attr("d", d3.link(curve)
                  .x(d => d.y)
                  .y(d => d.x));

        const node = svg.append("g")
          .selectAll("a")
          .data(root.descendants())
          .join("a")
            .attr("xlink:href", link == null ? null : d => link(d.data, d))
            .attr("target", link == null ? null : linkTarget)
            .attr("transform", d => `translate(${d.y},${d.x})`)


        node.append("circle")
            .attr("fill", d => d.children ? stroke : fill)
            .attr("r", r);
        node.append("title")
        .text(d => d.data.title);  // Assumes that your data has a 'title' property



        node.on("click", function (d,i) {
            // console.log("d,i="+d+" and i = "+i);
            console.log(i);
            console.log(i.data.name);
            // alert(i.data.summary);
            // USED!
            document.getElementById(`summary`).value = i.data.summary;

            //     // Update the text box content with node data (e.g., name)
        //     const textBox = document.getElementById("text-box"); // Update selector to match your text box element
        //     textBox.textContent = d.data.name; // Update with desired data property

        //     // Optional: Highlight clicked node (example using class)
        //     d3.select(this).classed("clicked", true);
        });



        if (title != null) node.append("title")
            .text(d => title(d.data, d));

        if (L) node.append("text")
            .attr("dy", "0.32em")
            .attr("x", d => d.children ? -6 : 6)
            .attr("text-anchor", d => d.children ? "end" : "start")
            .attr("paint-order", "stroke")
            .attr("stroke", halo)
            .attr("stroke-width", haloWidth)
            .text((d, i) => L[i])
            .each(function(d, i) {
                d3.select(this).on("click", function(event) {
                    // alert(L[i]);  // Print L[i] when the node is clicked
                    // document.getElementById(`summary`).value = L[i];
                });
            });

        return svg.node();
      }


    const url = 'http://0.0.0.0:8000/d3_data.json';
    fetch(url)
      .then(response => response.json())
      .then(data => {
        console.log(data);  // Log the parsed JSON data
        // Further processing of the data can be done here
        // For example, store it in a variable:
        const jsonData = data;
        console.log(jsonData);  // Verify that jsonData contains the data


    // This function creates a hierarchical tree visualization using the provided data.
    // It expects the data to be formatted as an object with nested objects (similar to the "flare.json" format).
    // Alternatively, it can handle tabular data (array of objects) if `id` and `parentId` options are provided for unique identification.
    // The function relies on the D3.js library for layout and rendering.
    let chart = Tree(data, {
        // Function to provide the display name for each node in the tree.
        label: d => d.name,

        // Function to generate hover text for each node.
        // It builds a string by joining the names of all ancestor nodes in reverse order, separated by dots (.).
        title: (d, n) => `${n.ancestors().reverse().map(d => d.data.name).join(".")}`,

        // Function to define the link URL for each node.
        // It constructs a URL based on the node's position in the hierarchy.
        // For leaf nodes (no children), it uses the ".as" extension.
        // link: (d, n) => `https://github.com/prefuse/Flare/${n.children ? "tree" : "blob"}/master/flare/src/${n.ancestors().reverse().map(d => d.data.name).join("/")}${n.children ? "" : ".as"}`,

        // Override the default width for the chart.
        // width: 1152
      });


    container.append(chart);
  })
  .catch(error => {
    console.error('Error fetching JSON data:', error);
  });

});
