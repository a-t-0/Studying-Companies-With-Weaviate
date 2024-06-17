# https:\_\_weaviate.io_developers_weaviate_api_rest_legacy_well-known

The live endpoint checks if the application is alive. You can use it for a Kubernetes liveness probe. The discovery endpoint accepts a GET request. If OpenID Connect (OIDC) authentication is enabled, the endpoint returns configuration details. If there is no OIDC provider, the Endpoint returns a 404 status code.
