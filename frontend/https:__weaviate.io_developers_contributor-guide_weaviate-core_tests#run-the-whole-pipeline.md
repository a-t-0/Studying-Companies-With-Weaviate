# https:\_\_weaviate.io_developers_contributor-guide_weaviate-core_tests#run-the-whole-pipeline

Weaviate Core uses a typical Test Pyramid approach. The tests are grouped into the following three levels:Unit tests test the smallest possible unit, mostly a struct in golang. Unit tests are designed to validate the business logic and not the internals.Integration tests test anything that crosses a boundary.
