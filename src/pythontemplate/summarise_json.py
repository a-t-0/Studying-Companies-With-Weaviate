# Source: https://weaviate.io/developers/weaviate/modules/reader-generator-modules/sum-transformers#in-short

from typing import Dict, List, Union

import weaviate
from typeguard import typechecked


def ask_weaviate_to_summarise(
    *,
    weaviate_local_host_url: str,
    json_object_name: str,
    summarised_property: str,
):
    """Working configuration:
    json_object_names="Question", summarised_property="theAnswer"
    """
    client = weaviate.Client(weaviate_local_host_url)
    print(f"json_object_name={json_object_name}")
    print(f"summarised_property={summarised_property}")
    result = client.query.get(
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
    ).do()
    return result


def inject_summarisation_into_website_graph(
    data,
    website_graph,
    max_nr_of_queries,
    json_object_name: str,
    summarised_property: str,
):
    vals = data["data"]["Get"][json_object_name]
    for i, node in enumerate(website_graph.nodes):
        # print(f'vals[i]=')
        if i < max_nr_of_queries:
            verify_summary_structure(
                single_summary=vals[i], summarised_property=summarised_property
            )
            original_main_text: str = get_original_text_from_summary_response(
                single_summary=vals[i], summarised_property=summarised_property
            )
            weaviate_summary: str = get_summary_response(
                single_summary=vals[i]
            )
            summary_url: str = get_summary_url(single_summary=vals[i])
            for node in website_graph.nodes:
                if node == summary_url:
                    website_graph.nodes[node]["summary"] = weaviate_summary
                    print(
                        f"website_graph.nodes[node]={website_graph.nodes[node]}"
                    )
                    if (
                        website_graph.nodes[node]["text_content"]
                        != original_main_text
                    ):
                        raise ValueError(
                            "The text_content values of summary and website graph don't match."
                        )


@typechecked
def verify_summary_structure(
    *,
    single_summary: Dict[str, Dict[str, Union[str, List[Dict[str, str]]]]],
    summarised_property: str,
):
    """Ensures a single summary contains the original text and the new summary
    in the correct position."""
    if "_additional" not in single_summary.keys():
        raise KeyError("_additional key containing Summary not found.")
    if "summary" not in single_summary["_additional"].keys():
        raise KeyError("summary key not found.")
    if len(single_summary["_additional"]["summary"]) != 1:
        raise ValueError(
            "The list of summaries does not contain a single element."
        )
    if "property" not in single_summary["_additional"]["summary"][0].keys():
        raise KeyError("property key not found in summary dictionary.")
    if (
        single_summary["_additional"]["summary"][0]["property"]
        != summarised_property
    ):
        raise KeyError(
            "The summary is made for a different property than the text_content."
        )
    if "result" not in single_summary["_additional"]["summary"][0].keys():
        raise KeyError("result key not found in summary dictionary.")
    if not isinstance(
        single_summary["_additional"]["summary"][0]["result"], str
    ):
        raise TypeError(
            "The value belonging to the result key was not a string."
        )
    if summarised_property not in single_summary.keys():
        raise KeyError("Original text not in element.")


def get_original_text_from_summary_response(
    *,
    single_summary: Dict[str, Dict[str, Union[str, List[Dict[str, str]]]]],
    summarised_property: str,
) -> str:
    """Returns the original main text that was extracted from the web page out
    of a Weaviate summary response.

    Assumes the single summary element has a valid structure.
    """
    return single_summary[summarised_property]


def get_summary_response(
    *, single_summary: Dict[str, Dict[str, Union[str, List[Dict[str, str]]]]]
) -> str:
    """Returns the Weaviate summary of the original main text that was
    extracted from the web page.

    Assumes the single summary element has a valid structure.
    """
    return single_summary["_additional"]["summary"][0]["result"]


def get_summary_url(
    *, single_summary: Dict[str, Dict[str, Union[str, List[Dict[str, str]]]]]
) -> str:
    """Returns the url belonging to the Weaviate summary.

    Assumes the single summary element has a valid structure.
    """
    return single_summary["url"]
