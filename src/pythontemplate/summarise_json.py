# Source: https://weaviate.io/developers/weaviate/modules/reader-generator-modules/sum-transformers#in-short

import weaviate
from pprint import pprint
from typeguard import typechecked
from typing import Dict, List, Union
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
    print("val=")
    pprint(val)
    for i, node in enumerate(website_graph.nodes):
        
        if i < max_nr_of_queries:
            verify_summary_structure(single_summary=val[i])
            original_main_text:str = get_original_text_from_summary_response(single_summary=val[i])
            weaviate_summary:str = get_summary_response(single_summary=val[i])
            print(f'node={node}')
            print("graph node=")
            pprint(website_graph.nodes[node])
            input("continue?")
            summary: str = val[i]["_additional"]["summary"][0]["result"]
            website_graph.nodes[node]["summary"] = summary

@typechecked
def verify_summary_structure(*, single_summary:Dict[str, Dict[str,Union[str, List[Dict[str,str]]]]]):
    """ Ensures a single summary contains the original text and the new summary in the correct position."""
    if "_additional" not in single_summary.keys():
        raise KeyError("_additional key containing Summary not found.")
    if "summary" not in single_summary["_additional"].keys():
        raise KeyError("summary key not found.")
    if  len(single_summary["_additional"]["summary"]) != 1:
        raise ValueError("The list of summaries does not contain a single element.")
    if "property" not in single_summary["_additional"]["summary"][0].keys():
        raise KeyError("property key not found in summary dictionary.")
    if  single_summary["_additional"]["summary"][0]["property"] != "text_content":
        raise KeyError("The summary is made for a different property than the text_content.")
    if "result" not in single_summary["_additional"]["summary"][0].keys():
        raise KeyError("result key not found in summary dictionary.")
    if not isinstance(single_summary["_additional"]["summary"][0]["result"],str):
        raise TypeError("The value belonging to the result key was not a string.")
    if "text_content" not in single_summary.keys():
        raise KeyError("Original text not in element.")
    
def get_original_text_from_summary_response(*, single_summary:Dict[str, Dict[str,Union[str, List[Dict[str,str]]]]]) -> str:
    """Returns the original main text that was extracted from the web page out
     of a Weaviate summary response.
     
    Assumes the single summary element has a valid structure."""
    return single_summary["text_content"]

def get_summary_response(*, single_summary:Dict[str, Dict[str,Union[str, List[Dict[str,str]]]]]) -> str:
    """Returns the Weaviate summary of the original main text that was extracted from the web page.
     
    Assumes the single summary element has a valid structure."""
    return single_summary["_additional"]["summary"][0]["result"]

def assert_summaries_have_no_duplicate_original_texts(*, summaries:List[Dict[str, Dict[str,Union[str, List[Dict[str,str]]]]]]) -> None:
    original_main_text:List[str] = list(map( lambda summary: get_original_text_from_summary_response(single_summary=summaries)))
    if not all_different(data = original_main_text):
        raise ValueError("Error, duplicate main texts found in summaries.")
    
def assert_website_graph_has_no_duplicate_original_texts(*, summaries:List[Dict[str, Dict[str,Union[str, List[Dict[str,str]]]]]]) -> None:
    original_main_text:List[str] = list(map( lambda summary: get_original_text_from_summary_response(single_summary=summaries)))
    if not all_different(data = original_main_text):
        raise ValueError("Error, duplicate main texts found in summaries.")


def all_different(*, data:List[str]) -> bool:
  """
  This function checks if all elements in a list are different using set conversion.

  Args:
      data: A list of strings.

  Returns:
      A boolean indicating if all elements are different.
  """
  return len(data) == len(set(data))