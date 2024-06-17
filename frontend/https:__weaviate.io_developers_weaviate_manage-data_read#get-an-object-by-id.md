# https:\_\_weaviate.io_developers_weaviate_manage-data_read#get-an-object-by-id

Use an ID to retrieve an object. If the id doesn't exist, Weaviate returns a 404 error. When multi-tenant datasets are enabled, the tenant name is required. If an object with a given id exists without retrieving it, make a HEAD request to the /v1/objects/ REST endpoint.
