# https:\_\_weaviate.io_blog_ann-algorithms-tiles-enocoder

In our previous post, we explained how to compress vectors in memory. We introduced HNSW+PQ and explained the most popular encoding technique: KMeans. The Tile encoder is a distribution-based encoder. It doesn’t need to be fit to the data since it leverages the underlying distribution of the data.
