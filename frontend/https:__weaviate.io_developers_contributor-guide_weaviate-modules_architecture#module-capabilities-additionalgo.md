# https:\_\_weaviate.io_developers_contributor-guide_weaviate-modules_architecture#module-capabilities-additionalgo

This page describes the code-level architecture of media2vec. The module architecture is dependent on the respective module. A module is essentially any struct that implements a specific Golang interface. The main interface is a really small one - a module essentially only has to provide a Name() string and Init(...) error method.
