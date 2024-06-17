# https:\_\_weaviate.io_developers_weaviate_configuration_monitoring#obtainable-metrics

Weaviate can expose Prometheus-compatible metrics for monitoring. A standard Prometheus/Grafana setup can be used to visualize metrics on various dashboards. Metrics are typically scraped into a time-series database, such as Prometheus. Weaviate will expose the metrics at <hostname>:2112/metrics.
