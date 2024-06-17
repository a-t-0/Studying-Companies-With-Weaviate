# https:\_\_weaviate.io_developers_weaviate_concepts_replication-architecture_motivation

Weaviate uses the Raft consensus algorithm for schema replication. This is a leader-based consensus algorithm, where a leader node is responsible for schema changes. Use of Raft ensures that schema changes are consistent across the cluster, even in the event of (a minority of) node failures.
