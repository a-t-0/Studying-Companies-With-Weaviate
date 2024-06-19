# https:\_\_weaviate.io_developers_academy_py_vector_index_dynamic

The dynamic index is a flat index that is automatically converted to an hnsw index when the number of vectors in the collection exceeds a predetermined threshold. The flat index is very efficient for small collections, but its search time increases linearly with the number. The hnSW index, on the other hand, is more efficient for large collections but includes a memory overhead.
