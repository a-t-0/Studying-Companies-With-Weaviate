# Source:
import weaviate
import weaviate.classes.config as wvcc

client = weaviate.connect_to_local()

try:
    # Note that you can use `client.collections.create_from_dict()` to create a collection from a v3-client-style JSON object
    collection = client.collections.create(
        name="TestArticle",
        vectorizer_config=wvcc.Configure.Vectorizer.text2vec_cohere(),
        generative_config=wvcc.Configure.Generative.cohere(),
        properties=[wvcc.Property(name="title", data_type=wvcc.DataType.TEXT)],
    )

finally:
    client.close()
