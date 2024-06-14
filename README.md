# Studying Companies with Weaviate Summary

[![Python 3.12][python_badge]](https://www.python.org/downloads/release/python-3120/)
[![License: AGPL v3][agpl3_badge]](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style: Black][black_badge]](https://github.com/ambv/black)

<p align="center">
  <img src="image.png" />

**“It is not daily increase but daily decrease, hack away the unessential.”**

</p>

______________________________________________________________________

This Weaviate workflow uses the summarise ✨ function by to speed up studying a company📚

- It takes in an url,
- Gets the complete website structure and stores the main content of each page into a networkx graph.
- This graph is then exported to a json file that is then uploaded to your local Weaviate instance.
- A GraphQL query is written that asks Weaviate to summarise the page content, which is then outputted into a new json and merged into the original graph.
- The graph is then reconverted into a mdbook to enable you to quickly develop a broad understanding of a company.

The summarised webpages are visualized in a tree structure in your self-hosted mdbook website🌐.

## Usage

To use this code, install the [prerequisites](prerequisites.md), and run [this](Summarise_website_with_weaviate.ipynb) Jupiter Notebook. Afterwards, you can show your website as summarised by Weaviate with:

```sh
mdbook build &&  mdbook serve
```

(Ps. You can also run `python -m src.pythontemplate` if you prefer CLI over ipynb).

## Example 1

**Before:**

![Before Image](images/b0.png)

**After:**

![After Image](images/a0.png)

## Another example

**Before:**

![Before Image](images/b1.png)

**After:**

![After Image](images/a1.png)

Ps. The summary texts are swapped, because I use indexes instead of node texts
to add the summaries, and I expect pre-commit sorted the `.json` file inbetween.

## How can this be made more awesome?🚀

- Represent tree structure in mdbook.
- Count number of links to- & from page, and visualize it in edge thickness in a (PlantUml) tree/ table of contents.
- Most of the time, it is not just the raw data you want from a company website but the secondary (or ternary) insights gained in processing that data and/or combining it with other relevant or recent developments. This is where Weaviate may shine, as it supports enhancing your own databases in combination with LLMs. A guided structure may be set up to facilitate this.

[agpl3_badge]: https://img.shields.io/badge/License-AGPL_v3-blue.svg
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[python_badge]: https://img.shields.io/badge/python-3.6-blue.svg
