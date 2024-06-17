# https:\_\_weaviate.io_blog_zero-downtime-upgrades

Weaviate has a robust, production-ready database that can scale as our users do. For example, many of our users already run Weaviate with multi-tenancy (introduced in version 1.20) to host thousands of active tenants or even more. One side effect of scaling is that as load increases on each node, it will take longer to start up.
