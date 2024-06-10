# Source: https://weaviate.io/developers/weaviate/modules/reader-generator-modules/sum-transformers#in-short

import weaviate


def ask_weaviate_to_summarise(
    *, weaviate_local_host_url: str, json_type: str, type_property: str
):
    """Working configuration:
    json_types="Question", type_property="theAnswer"
    """
    client = weaviate.Client(weaviate_local_host_url)

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


def inject_summarisation_into_website_graph(
    data, website_graph, max_nr_of_queries
):
    val = data["data"]["Get"]["Nodes"]

    for i, node in enumerate(website_graph.nodes):
        if i < max_nr_of_queries:
            summary: str = val[i]["_additional"]["summary"][0]["result"]
            website_graph.nodes[node]["summary"] = summary
