# Prerequisites

This contains the installation instructions needed to run the Jupyter Notebook (on Ubuntu).

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

## Frontend

run:

```sh
mdbook build &&  mdbook serve
```

to show the website you want to study, as a tree with leafs summarised by weaviate.
