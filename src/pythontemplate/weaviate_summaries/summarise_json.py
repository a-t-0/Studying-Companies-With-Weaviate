from typing import Dict, List, Union

import networkx as nx
import weaviate
from typeguard import typechecked
from weaviate import Client

from src.pythontemplate.load_json_into_weaviate.import_local_json import (
    get_hash,
)


def ask_weaviate_to_summarise(
    *,
    weaviate_local_host_url: str,
    json_object_name: str,
    summarised_property: str,
) -> Dict[str, Dict[str, Dict[str, List]]]:  # type: ignore[type-arg]
    """Working configuration:

    json_object_names="Question", summarised_property="theAnswer"
    """
    client = weaviate.Client(weaviate_local_host_url)

    client.query.get(json_object_name)
    urls = [
        obj["url"]
        for obj in client.query.get(json_object_name, ["url"])
        .with_limit(1000)
        .do()["data"]["Get"][json_object_name]
    ]

    summarised_json: Dict[  # type: ignore[type-arg]
        str, Dict[str, Dict[str, List]]
    ] = {"data": {"Get": {"WebPage": []}}}
    if len(urls) != len(list(set(urls))):
        raise ValueError("Duplicate url found.")

    for i, url in enumerate(urls):
        print(f"i={i}, url={url}")

        result = weaviate_summary_query_on_single_text(
            client,
            json_object_name,
            summarised_property,
            get_hash(some_str=url),
        )

        summarised_json["data"]["Get"]["WebPage"].append(
            result["data"]["Get"]["WebPage"][0]
        )
    return summarised_json


def weaviate_summary_query_on_single_text(
    client: Client,
    json_object_name: str,
    summarised_property: str,
    url_hash: str,
) -> Dict:  # type: ignore[type-arg]
    result: Dict = (  # type: ignore[type-arg]
        client.query.get(
            json_object_name,
            [
                summarised_property,
                (
                    '_additional { summary ( properties: ["'
                    + summarised_property
                    + '"]) { property result } }'
                ),
                "url",
            ],
        )
        .with_where(
            {
                "path": ["urlHash"],
                "operator": "Equal",
                # url hash is used because equal behaves as contains.
                "valueText": url_hash,
            }
        )
        .do()
    )
    return result


@typechecked
def inject_summarisation_into_website_graph(
    data: Dict,  # type: ignore[type-arg]
    website_graph: nx.DiGraph,
    max_nr_of_queries: int,
    json_object_name: str,
    summarised_property: str,
) -> None:

    vals = data["data"]["Get"][json_object_name]
    print(f"len(vals)={len(vals)}")
    for i, node in enumerate(website_graph.nodes):
        if i < max_nr_of_queries:

            original_main_text: str = get_original_text_from_summary_response(
                single_summary=vals[i], summarised_property=summarised_property
            )
            weaviate_summary: str = get_summary_response(
                single_summary=vals[i]
            )
            summary_url: str = get_summary_url(single_summary_with_url=vals[i])
            for node in website_graph.nodes:
                if node == summary_url:
                    website_graph.nodes[node]["summary"] = weaviate_summary

                    if (
                        website_graph.nodes[node]["text_content"]
                        != original_main_text
                    ):
                        print(
                            "website_graph.nodes[node]="
                            + f"{website_graph.nodes[node]}"
                        )
                        raise ValueError(
                            "The text_content values of summary and website"
                            " graph don't match."
                        )


def get_original_text_from_summary_response(
    *,
    single_summary: Dict[str, Dict[str, Union[str, List[Dict[str, str]]]]],
    summarised_property: str,
) -> str:
    """Returns the original main text that was extracted from the web page out
    of a Weaviate summary response.

    Assumes the single summary element has a valid structure.
    """
    if not isinstance(single_summary, dict):
        raise TypeError("Expected Dict.")
    if not isinstance(single_summary[summarised_property], str):
        raise TypeError(
            "Expected summarized property to be a string,"
            + f" yet it was:{single_summary} of type:{type(single_summary)}."
        )
    return str(single_summary[summarised_property])


def get_summary_response(
    *, single_summary: Dict[str, Dict[str, Union[str, List[Dict[str, str]]]]]
) -> str:
    """Returns the Weaviate summary of the original main text that was
    extracted from the web page.

    Assumes the single summary element has a valid structure.
    """
    if len(single_summary["_additional"]["summary"]) > 0:
        if not isinstance(single_summary, dict):
            raise TypeError("Expected Dict.")
        if not isinstance(single_summary["_additional"], dict):
            raise TypeError("Expected Dict in additional.")
        if not isinstance(single_summary["_additional"]["summary"], List):
            raise TypeError("Expected List.")
        if not isinstance(single_summary["_additional"]["summary"][0], dict):
            raise TypeError("Expected Dict within List.")
        if not isinstance(
            single_summary["_additional"]["summary"][0]["result"], str
        ):
            raise TypeError("Expected the summary response to be a string.")
        return single_summary["_additional"]["summary"][0]["result"]
    else:
        return "No web page text found, so no summary available."


def get_summary_url(
    *,
    single_summary_with_url: Dict[
        str, Dict[str, Union[str, List[Dict[str, str]]]]
    ],
) -> str:
    """Returns the url belonging to the Weaviate summary.

    Assumes the single summary element has a valid structure.
    """
    if not isinstance(single_summary_with_url["url"], str):
        raise TypeError("Expected the url to be a string.")
    return single_summary_with_url["url"]
