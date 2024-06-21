# Source: https://weaviate.io/developers/weaviate/tutorials/import

import hashlib
import json
from typing import Collection, Dict, List, Sequence

import weaviate
from typeguard import typechecked

from src.pythontemplate.helper import get_output_path


@typechecked
def load_local_json_data_into_weaviate(
    *,
    weaviate_local_host_url: str,
    company_url: str,
    output_dir: str,
    json_input_path: str,
    json_object_name: str,
    summarised_property: str,
) -> None:
    """Loads and parses a file in JSON format and stores it in Weaviate.

    Args: :weaviate_local_host_url: (str), The URL of the local Weaviate
    instance. :json_input_path: (str), The path to the JSON file that should be
    loaded. :json_object_name: (str), The name of the object type in Weaviate
    that the data should be stored under. :summarised_property: (str), The
    property in the JSON data that represents the summary of the object.
    """
    nx_json_output_path: str = get_output_path(
        output_dir=output_dir,
        company_url=company_url,
        filename=json_input_path,
    )
    client = weaviate.Client(
        url=weaviate_local_host_url,
    )

    try:
        with open(nx_json_output_path) as f:
            data: Dict = json.load(f)  # type: ignore[type-arg]
    except FileNotFoundError:
        print(f"Error: File '{nx_json_output_path}' not found.")
        exit()

    add_imported_json_graph_to_weaviate(
        client=client,
        data=data,
        json_object_name=json_object_name,
        summarised_property=summarised_property,
    )


@typechecked
def add_imported_json_graph_to_weaviate(
    *,
    client: weaviate.Client,
    data: Dict,  # type: ignore[type-arg]
    json_object_name: str,
    summarised_property: str,
) -> None:
    """Adds the imported JSON data as a graph to Weaviate.

    Args: :client: (weaviate.Client), The client used to communicate with
    Weaviate. :data: (Dict), The dictionary containing the JSON data to be
    imported. :json_object_name: (str), The name of the JSON object in
    Weaviate. :summarised_property: (str), The property used to generate
    summaries for the objects. Returns: None
    """

    remove_existing_schemas_from_weaviate(client=client)
    schema: Dict[str, Sequence[Collection[str]]] = create_new_schema(
        json_object_name=json_object_name,
        summarised_property=summarised_property,
    )

    add_schema(client, schema)
    weaviate_data_objects: List[Dict] = (  # type: ignore[type-arg]
        create_weaviate_formatted_data_objects(
            data=data,
            summarised_property=summarised_property,
        )
    )
    add_weviate_data_objects_to_weaviate(
        client=client,
        weaviate_data_objects=weaviate_data_objects,
        json_object_name=json_object_name,
    )


@typechecked
def remove_existing_schemas_from_weaviate(client: weaviate.Client) -> None:
    """Removes all pre-existing schemas from Weaviate.

    A schema is a dictionary that describes the structure of the data in
    Weaviate. It typically starts with a class (e.g. Document), and then such a
    class has properties. A class property in a schema has (at least) a name,
    and a datatype.
    """
    client.schema.delete_all()


@typechecked
def create_new_schema(
    json_object_name: str, summarised_property: str
) -> Dict[str, Sequence[Collection[str]]]:
    """Creates a new schema for a JSON object with the given name.

    Args: :json_object_name: (str), The name of the JSON object.
    :summarised_property: (str), The property that will be used to summarise
    the JSON object. Returns: The new schema for the JSON object.
    """

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


@typechecked
def add_schema(
    client: weaviate.Client, schema: Dict[str, Sequence[Collection[str]]]
) -> None:
    """Adds a schema to a Weaviate client.

    Args: :client: (Weaviate.Client), A Weaviate client. :schema: (Dict[str,
    Sequence[Collection[str]]]), A schema represented as a dictionary mapping
    class names to lists of property paths.
    """

    client.schema.create_class(schema)


@typechecked
def create_weaviate_formatted_data_objects(
    data: Dict, summarised_property: str  # type: ignore[type-arg]
) -> List[Dict]:  # type: ignore[type-arg]
    """Assumes all nodes belong to unique addresses."""
    weaviate_data_objects: List[Dict] = []  # type: ignore[type-arg]
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


@typechecked
def get_hash(some_str: str) -> str:
    return hashlib.sha256(some_str.encode()).hexdigest()


@typechecked
def add_weviate_data_objects_to_weaviate(
    client: weaviate.Client,
    weaviate_data_objects: List[Dict],  # type: ignore[type-arg]
    json_object_name: str,
) -> None:

    with client.batch as batch:
        for data_object in weaviate_data_objects:
            batch.add_data_object(data_object, json_object_name)
