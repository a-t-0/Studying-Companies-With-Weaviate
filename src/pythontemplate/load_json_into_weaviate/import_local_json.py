# Source: https://weaviate.io/developers/weaviate/tutorials/import

import hashlib
import json
from typing import Dict, List

import weaviate


def load_local_json_data_into_weaviate(
    *,
    weaviate_local_host_url: str,
    json_input_path: str,
    json_object_name: str,
    summarised_property: str,
):
    client = weaviate.Client(
        url=weaviate_local_host_url,
        # additional_headers={
        # "X-OpenAI-Api-Key": "YOUR-OPENAI-API-KEY"  # Or "X-Cohere-Api-Key" or "X-HuggingFace-Api-Key"
        # }
    )

    # Open the file in read mode
    try:
        with open(json_input_path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_input_path}' not found.")
        exit()

    add_imported_json_graph_to_weaviate(
        client=client,
        data=data,
        json_object_name=json_object_name,
        summarised_property=summarised_property,
    )


# Source 0: https://github.com/weaviate/recipes/blob/0b1542fad2f03f9316ccd52290f148397cb8c346/integrations/llm-frameworks/dspy/blog/2023-05-23-pdfs-to-weaviate/index.mdx#L266
# Source 0.1: https://github.com/weaviate-tutorials/how-to-ingest-pdfs-with-unstructured/blob/main/notebooks/01_blog.ipynb
def add_imported_json_graph_to_weaviate(
    *,
    client: weaviate.Client,
    data,
    json_object_name: str,
    summarised_property: str,
) -> None:
    remove_existing_schemas_from_weaviate(client=client)
    schema: Dict = create_new_schema(
        json_object_name=json_object_name,
        summarised_property=summarised_property,
    )
    # schema: Dict = create_new_schema_with_summary(
    # json_object_name=json_object_name,
    # summarised_property=summarised_property,
    # )

    add_schema(client, schema)
    # verify_data_satisfies_schema(data=data, schema=schema)
    weaviate_data_objects: List[Dict] = create_weaviate_formatted_data_objects(
        data=data,
        summarised_property=summarised_property,
    )
    add_weviate_data_objects_to_weaviate(
        client=client,
        weaviate_data_objects=weaviate_data_objects,
        json_object_name=json_object_name,
    )


def remove_existing_schemas_from_weaviate(client: weaviate.Client) -> None:
    """Removes all pre-existing schemas from Weaviate.

    A schema is a dictionary that describes the structure of the data in
    Weaviate. It typically starts with a class (e.g. Document), and then such a
    class has properties. A class property in a schema has (at least) a name,
    and a datatype.
    """
    client.schema.delete_all()


def create_new_schema(json_object_name: str, summarised_property: str) -> Dict:
    schema = {
        "class": json_object_name,
        "properties": [
            {
                "name": "url",
                "dataType": ["text"],
            },
            {
                "name": "urlHash",
                "dataType": ["text"],
            },
            {
                "name": summarised_property,
                "dataType": ["text"],
            },
        ],
    }
    return schema


def create_new_schema_with_summary(
    json_object_name: str, summarised_property: str
) -> Dict:
    schema = {
        "class": json_object_name,
        "vectorizer": "text2vec-openai",
        "properties": [
            {
                "name": "url",
                "dataType": ["text"],
            },
            {
                "name": "urlHash",
                "dataType": ["text"],
            },
            {
                "name": summarised_property,
                "dataType": ["text"],
                "moduleConfig": {
                    "text2vec-openai": {
                        "skip": False,
                        "vectorizePropertyName": False,
                    }
                },
            },
        ],
        "moduleConfig": {
            "generative-openai": {},
            "text2vec-openai": {
                "model": "ada",
                "modelVersion": "002",
                "type": "text",
            },
        },
    }
    return schema


def add_schema(client: weaviate.Client, schema: Dict) -> None:
    client.schema.create_class(schema)


def create_weaviate_formatted_data_objects(
    data, summarised_property: str
) -> List[Dict]:
    """Assumes all nodes belong to unique addresses."""
    weaviate_data_objects: List[Dict] = []
    for webpage in data["nodes"]:
        if "text_content" in webpage.keys():
            data_object = {
                "url": webpage["id"],
                "urlHash": get_hash(some_str=webpage["id"]),
                # text_content is how networkx stores the node attribute.
                summarised_property: webpage["text_content"],
            }
            weaviate_data_objects.append(data_object)
    return weaviate_data_objects


def get_hash(some_str: str):
    return hashlib.sha256(some_str.encode()).hexdigest()


def add_weviate_data_objects_to_weaviate(
    client: weaviate.Client,
    weaviate_data_objects: List[Dict],
    json_object_name: str,
):

    with client.batch as batch:
        for data_object in weaviate_data_objects:
            batch.add_data_object(data_object, json_object_name)
