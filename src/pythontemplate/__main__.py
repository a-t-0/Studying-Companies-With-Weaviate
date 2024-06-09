"""Entry point for the project."""
from typing import List
from src.pythontemplate.get_local_json_data import website_to_json


company_urls:List[str] = ["https://weaviate.io/"]
json_output_path:str = "weaviate.json"
weaveate_local_host_url:str="http://localhost:8080"

# Get the json data.
# website_to_json(urls=company_urls, json_output_path=json_output_path)
visited = set() # Initialise an empty website set.
website_to_json(url=company_urls[0], output_file=json_output_path, visited=visited)
print(f"Crawled company website and stored results in:{json_output_path}")

# Structure the json data
# structure_json_data(json_input_path=json_output_path)

# Ensure the json data is loaded into weaviate.
load_local_json_data_into_weaviate(json_input_path=json_output_path)

# Limit the number of queries to summarise to 3.
max_nr_of_queries:int = 3

# Perform queries to summarise the data.
summarised_data = ask_weaviate_to_summarise(json_input_path=json_output_path)

# Generate plantUML or (md books) website for company.
generate_summarised_company_website(summarised_data=summarised_data)