# https:\_\_weaviate.io_developers_academy_py_starter_multimodal_data_mm_collections_import_data

This example imports the movie data into our collection. We use the requests library to load the data from the source. The text data is then converted to a Pandas DataFrame. The images are extracted from the Zip file. Then, we create a collection object (with client.collections.get) so we can interact with the collection.
