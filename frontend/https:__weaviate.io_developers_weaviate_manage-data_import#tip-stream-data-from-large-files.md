# https:\_\_weaviate.io_developers_weaviate_manage-data_import#tip-stream-data-from-large-files

Batch imports are an efficient way to add multiple data objects and cross-references. The Python clients have built-in batching methods to help you optimize import speed. If your dataset is large, consider streaming the import to avoid out-of-memory issues.
