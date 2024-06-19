# https:\_\_weaviate.io_developers_weaviate_api_graphql_additional-operators#autocut

Pagination is not a cursor-based implementation. This has the following implications: The autocut function limits results based on discontinuities in the result set. The query stops returning results after the specified number of jumps. The Get and Explore functions support offset. For more details, see performance considerations.
