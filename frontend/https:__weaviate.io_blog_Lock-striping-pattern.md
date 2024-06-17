# https:\_\_weaviate.io_blog_Lock-striping-pattern

Weaviate is a database with hundreds of millions of data objects. Weaviate must be able to import data quickly and reliably while maintaining data integrity and reducing time overhead. Database design comes with interesting challenges. Lock striping is an arrangement where locking occurs on multiple buckets or 'stripes'
