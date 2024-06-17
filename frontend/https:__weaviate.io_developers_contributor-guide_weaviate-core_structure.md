# https:\_\_weaviate.io_developers_contributor-guide_weaviate-core_structure

Weaviate's package structure is modelled after CleanArchitecture. The most central "entities" are found in the ./entities subpackages. All of these packages areagnostic of the API-types (GraphQL, REST, etc) as well as the usecases/kinds package.
