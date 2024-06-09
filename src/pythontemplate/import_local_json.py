# Source: https://weaviate.io/developers/weaviate/tutorials/import

import json

import weaviate

client = weaviate.Client(
    url="http://localhost:8080",  # Replace with your Weaviate endpoint
    # additional_headers={
    # "X-OpenAI-Api-Key": "YOUR-OPENAI-API-KEY"  # Or "X-Cohere-Api-Key" or "X-HuggingFace-Api-Key"
    # }
)

import json

# ===== import data =====
# Load data

# Path to your local JSON file
filename = "minimal.json"

# Open the file in read mode
try:
    with open(filename) as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    exit()


# Prepare a batch process
print(f"client={client}")
print(f"client={client.__dict__}")
print(f"client={client.query.__dict__}")
client.batch.configure(batch_size=100)  # Configure batch
with client.batch as batch:
    # Batch import all Questions
    for i, d in enumerate(data):
        # print(f"importing question: {i+1}")  # To see imports
        if i < 3:
            properties = {
                "theAnswer": d["Answer"],
                "theQuestion": d["Question"],
                "theCategory": d["Category"],
            }

            batch.add_data_object(properties, "Question")
