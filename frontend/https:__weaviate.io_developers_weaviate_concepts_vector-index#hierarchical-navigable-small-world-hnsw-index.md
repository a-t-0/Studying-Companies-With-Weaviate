# https:\_\_weaviate.io_developers_weaviate_concepts_vector-index#hierarchical-navigable-small-world-hnsw-index

Weaviate's vector-first storage system takes care of all storage operations with a vector index. The dynamic index can even start off as a flat index and then dynamically switch to the HNSW index as it scales past a threshold. Weavia supports two types of vector indexing:Available starting in v1.25.
