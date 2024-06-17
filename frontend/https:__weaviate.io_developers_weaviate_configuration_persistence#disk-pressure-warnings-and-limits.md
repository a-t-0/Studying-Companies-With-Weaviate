# https:\_\_weaviate.io_developers_weaviate_configuration_persistence#disk-pressure-warnings-and-limits

When running Weaviate with Docker or Kubernetes, you can persist its data by mounting a volume to store the data outside of the containers. Doing so will cause the Weaviates instance to also load the data from the mounted volume when it is restarted.
