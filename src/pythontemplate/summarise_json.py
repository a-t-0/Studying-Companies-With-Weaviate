# Source: https://weaviate.io/developers/weaviate/modules/reader-generator-modules/sum-transformers#in-short
from pprint import pprint

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


def inject_summarisation_into_website_graph(data, website_graph):
    val = data["data"]["Get"]["Nodes"]
    pprint(f"val={val}")
    # print(f'data={data}')
    for i, node in enumerate(website_graph.nodes):
        pprint(f"i={i}, node={node}")
        if i < 3:
            summary: str = val[i]["_additional"]["summary"][0]["result"]
            website_graph.nodes[node]["summary"] = summary
            print(f"added summary:{summary}")
            # val[i]
            print("website_graph.nodes[node]:")
            # pprint(website_graph.nodes[node]["summary"])
            pprint(website_graph.nodes[node])
