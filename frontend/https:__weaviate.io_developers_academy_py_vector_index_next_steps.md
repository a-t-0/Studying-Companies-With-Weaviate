# https:\_\_weaviate.io_developers_academy_py_vector_index_next_steps

When choosing an index type, use the following as a guide. In a multi-tenant environment, the "dynamic" index may be a good default choice, as it will allow some tenants to remain in the flat index while others are automatically converted to hnsw when they grow.
