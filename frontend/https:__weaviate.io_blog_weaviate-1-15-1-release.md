# https:\_\_weaviate.io_blog_weaviate-1-15-1-release

Two weeks after the v1.15.0 release, which introduced backups and more, we fixed over 15 bugs. This release addresses fixes and improvements around: This started as a single bug investigation, but quickly this led to a discovery of five others. There was an issue when trying to update objects without vectors, but then you would add a vector later. That could lead to cryptic error messages like "incompatible vector dimensions: 0 vs. 128".
