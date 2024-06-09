# Source: https://weaviate.io/developers/weaviate/tutorials/import

import json

import weaviate

client = weaviate.Client(
    url="http://localhost:8080",  # Replace with your Weaviate endpoint
    # additional_headers={
    # "X-OpenAI-Api-Key": "YOUR-OPENAI-API-KEY"  # Or "X-Cohere-Api-Key" or "X-HuggingFace-Api-Key"
    # }
)

# ===== import data =====
# Load data
import requests

url = "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
resp = requests.get(url)
data = json.loads(resp.text)

# Prepare a batch process
client.batch.configure(batch_size=100)  # Configure batch
with client.batch as batch:
    # Batch import all Questions
    for i, d in enumerate(data):
        # print(f"importing question: {i+1}")  # To see imports

        properties = {
            "Answer": d["Answer"],
            "Question": d["Question"],
            "Category": d["Category"],
        }

        batch.add_data_object(properties, "Question")
