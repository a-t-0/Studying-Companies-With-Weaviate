# https:\_\_weaviate.io_developers_weaviate_concepts_modules

Weaviate has a modularized structure. Functionality such as vectorization or backups is handled by optional modules. Weaviate does not know how to vectorize an object, i.e. how to calculate the vectors given an object. You can choose and attach a vectorizer module that best fits your use case.
