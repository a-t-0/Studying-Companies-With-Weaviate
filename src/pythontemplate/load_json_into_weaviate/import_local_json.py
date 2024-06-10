# Source: https://weaviate.io/developers/weaviate/tutorials/import

import json

import weaviate


def load_local_json_data_into_weaviate(
    *,
    weaveate_local_host_url: str,
    json_input_path: str,
    json_type: str,
    type_property: str,
):
    client = weaviate.Client(
        url=weaveate_local_host_url,
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

    # Prepare a batch process
    client.batch.configure(batch_size=100)  # Configure batch
    with client.batch as batch:

        # Batch import all Questions
        for i, node in enumerate(data["nodes"]):
            input(f"data elem ={node}")
            if i < 3:
                # TODO: verify the data element is not already in weaviate.
                try:
                    properties = {
                        # type_property: d["Answer"],
                        type_property: node["text_content"],
                        # type_property: json_type,
                    }

                    batch.add_data_object(properties, json_type)
                except:
                    print(f"Skipped data element:{node}")
