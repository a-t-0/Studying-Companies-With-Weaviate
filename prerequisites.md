# Prerequisites

This contains the installation instructions needed to run the Jupyter Notebook (on Ubuntu).

## Weaviate usage

Copy/create the relevant docker filecontent from the [website](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/sum-transformers) into `docker-compose.yml`.

```sh
# Install the conda environment with the packages used in this repo.
conda env create --file environment.yml
conda activate pythontemplate

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

## Devs

To use the tools used to develop this repo, one can use:

```sh
pre-commit install
npm init

sudo apt install eslint
npm init @eslint/config@latest
```
