# https:\_\_weaviate.io_developers_weaviate_concepts_reranking

Reranking seeks to improve search relevance by reordering the result set returned by a retriever with a different model. It computes a relevance score between the query and each data object, and returns the list of objects sorted from the most to the least relevant. With our reranker modules, you can conveniently perform multi-stage searches without leaving Weaviate.
