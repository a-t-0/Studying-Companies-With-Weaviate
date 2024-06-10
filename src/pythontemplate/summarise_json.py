# Source: https://weaviate.io/developers/weaviate/modules/reader-generator-modules/sum-transformers#in-short
import weaviate


def ask_weaviate_to_summarise(
    *, weaveate_local_host_url: str, json_type: str, type_property: str
):
    """Working configuration:
    json_types="Question", type_property="theAnswer"
    """
    # TODO: check if the data is already loaded.
    client = weaviate.Client(weaveate_local_host_url)

    result = client.query.get(
        json_type,
        [
            type_property,
            (
                '_additional { summary ( properties: ["'
                + type_property
                + '"]) { property result } }'
            ),
        ],
    ).do()
    return result
