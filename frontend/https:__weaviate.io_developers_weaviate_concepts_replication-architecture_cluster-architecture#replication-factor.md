# https:\_\_weaviate.io_developers_weaviate_concepts_replication-architecture_cluster-architecture#replication-factor

Weaviate uses the Raft consensus algorithm for schema replication, implemented with Hashicorp's raft library. A schema change is forwarded to the leader node, which applies the change to its log before replicating it to the follower nodes. This architecture ensures that schema changes are consistent across the cluster, even in the event of (a minority of) node failures.
