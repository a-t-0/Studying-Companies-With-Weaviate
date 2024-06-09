# Source: https://weaviate.io/developers/weaviate/modules/reader-generator-modules/sum-transformers#in-short
import weaviate

client = weaviate.Client("http://localhost:8080")

result = client.query.get(
    "Question",
    [
        "theAnswer",
        (
            '_additional { summary ( properties: ["theAnswer"]) { property'
            " result } }"
        ),
    ],
).do()

print(result)
