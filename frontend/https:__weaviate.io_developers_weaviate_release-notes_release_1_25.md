# https:\_\_weaviate.io_developers_weaviate_release-notes_release_1_25

In 1.25 we’re introducing the dynamic vector index. This will initially create a flat index to be used and once the number of objects exceeds a certain threshold (by default 10,000 objects) it will dynamically switch you over to an HNSW index. Here is how you can configure Weaviate to use a dynamic index.
