# https:\_\_weaviate.io_developers_weaviate_manage-data_multi-tenancy#update-tenant-activity-status

Multi-tenancy provides data isolation. Each tenant is stored on a separate shard. Data stored in one tenant is not visible to another tenant. Weaviate returns an error if you try to insert an object into a non-existent tenant. The auto-tenant feature is available from v1.25.0 for batch imports.
