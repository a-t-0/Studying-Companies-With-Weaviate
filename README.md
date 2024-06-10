# Studying Companies with Weaviate Summary
[![Python 3.12][python_badge]](https://www.python.org/downloads/release/python-3120/)
[![License: AGPL v3][agpl3_badge]](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style: Black][black_badge]](https://github.com/ambv/black)

Dear reader, hi! 

This will work as of 2024-06-10T15:00 CEST. It is a workflow that uses the summarise function by Weaviate to speed up studying a company.
- It takes in an url,
- Crawls that entire webiste for subdomains and stores its content into a json file.
- This json file is then uploaded to your local Weaviate instance.
- Then it uses GraphQL to get summaries of the company website structure.
- This summarised website structure is then reconverted into a simplified mdbook to enable you to quicly develop a broad understanding of a company.

## How can this be made more awesome?
 - First of all the code can be decluttered by converting it into a simple runnable `.ipynb`.
 - Most of the time, it is not just the raw data you want from a company website but the secondary (or ternary) insights gained in processing that data and/or combining it with other relevant or recent developments. This is where Weaviate may shine, as it supports enhancing your own databases in combination with LLMs. A guided structure may be set up to facilitate this.


## Weaviate usage

Copy/create the relevant docker filecontent from the [website](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/sum-transformers) into `docker-compose.yml`.

```sh
# Install docker
sudo apt install docker-compose
# Run the first docker-compose file that is given.
docker-compose up -d
# Install weaviate
pip install -U weaviate-client  # For beta versions: `pip install --pre -U "weaviate-client==4.*"`
```
Then you can use basic Weaviate.

## Clear Weaviate database

Instead of writing a proper delete function, change `QUERY_DEFAULTS_LIMIT: 35` in `docker-compose.yml` and
reinitialise the Weaviate docker with:

```sh
docker-compose up -d
```

## Summation

[Source.](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/sum-transformers) To use the summation feature, you also need to make sure something can do the summation.
To do this, create a file named:

```txt
my-model.Dockerfile
```

with content:

```Dockerfile
FROM semitechnologies/sum-transformers:custom
RUN chmod +x ./download.py
RUN MODEL_NAME=google/pegasus-pubmed ./download.py
```

and run and build it with:

```sh
docker build -f my-model.Dockerfile -t google-pegasus-pubmed .
```

Then you can verify your summation module works, by `UNKNOWN`. You can use this
summation module in other docker files by referring to its tag: `google-pegasus-pubmed`.
I do not yet know how exactly.

## Usage

First install this pip package with:

```bash
pip install pythontemplate
```

Then run:

```sh
python -m src.pythontemplate
```

[agpl3_badge]: https://img.shields.io/badge/License-AGPL_v3-blue.svg
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[python_badge]: https://img.shields.io/badge/python-3.6-blue.svg
