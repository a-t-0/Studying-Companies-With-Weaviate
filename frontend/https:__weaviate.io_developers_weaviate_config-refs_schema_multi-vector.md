# https:\_\_weaviate.io_developers_weaviate_config-refs_schema_multi-vector

Weaviate collections support multiple, named vectors. Each vector space has its own index, its own compression, and its own vectorizer. This means you can create vectors for properties, use different vectorization models, and apply different metrics to the same object. Single vector collections are valid and continue to use the original collection syntax.
