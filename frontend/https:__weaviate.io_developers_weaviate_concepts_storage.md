# https:\_\_weaviate.io_developers_weaviate_concepts_storage

Weaviate is a persistent and fault-tolerant database. This page gives you an overview of how objects and vectors are stored within Weaviate and how an inverted index is created at import time. Each class in Weaviates user-defined schema leads to the creation of an index internally. An index is a wrapper type comprised of one or many shards.
