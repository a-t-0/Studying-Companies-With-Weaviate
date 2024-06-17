# https:\_\_weaviate.io_developers_academy_py_starter_custom_vectors_object_rag_single_prompt

A 'single prompt' generation wil perform RAG queries on each retrieved object. This is useful when you want to transform each object separately, with the same prompt. This example finds entries in "Movie" based on their similarity to the input vector. Then, instructs the large language model to translate the title of each movie into French.
