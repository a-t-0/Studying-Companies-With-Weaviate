# https:\_\_weaviate.io_developers_academy_py_vector_index_flat

The flat index is a very simple vector index that mimics a "map" data type. It simply stores the location of each vector, such that a search can be done by comparing the query vector to each vector in the collection. This leads to very low resource requirements, at the cost of search speed as the number of vectors increases.
