# https:\_\_weaviate.io_developers_weaviate_more-resources_migration_weaviate-1-25

Weaviate 1.25 introduces RAFT as the consensus algorithm for its database. This change requires a migration of the entire schema. The cluster requires some downtime for the migration. The length of the downtime depends on the size of the database. We suggest performing this upgrade at a least disruptive time.
