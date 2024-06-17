# https:\_\_weaviate.io_developers_academy_py_starter_text_data_text_collections_import_data

This example uses the .dynamic() method to create a dynamic batcher, which automatically determines and updates the batch size during the import process. There are also other batcher types, like .fixed_size() for specifying the number of objects per batch. The data is converted from a string to the correct data types for Weaviate.
