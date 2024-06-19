# https:\_\_weaviate.io_developers_academy_py_compression_strategy

PQ is currently only supported for the HNSW index. If you are using the flat index, you will need to use BQ. PQ parameters are tunable whereas BQ is not. This means you can adjust PQ to be more or less aggressive on performance parameters.
