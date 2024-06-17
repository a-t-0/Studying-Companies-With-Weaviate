# https:\_\_weaviate.io_developers_academy_py_starter_text_data_text_rag_single_prompt

A 'single prompt' generation wil perform RAG queries on each retrieved object. This is useful when you want to transform each object separately, with the same prompt. This example finds entries in "Movie" whose vector best matches the query vector (for "dystopian future"). Then, instructs the large language model to translate the title of each movie into French.
