# https:\_\_weaviate.io_developers_contributor-guide_weaviate-core_parsing-cross-refs

Objects are parsed twice: First, closest to disk, immediately after reading-in the byte blob. A second time at the root level of the db.DB type, the whole request is parsed again (recursively) and cross-refs are resolved as requested by the user.
