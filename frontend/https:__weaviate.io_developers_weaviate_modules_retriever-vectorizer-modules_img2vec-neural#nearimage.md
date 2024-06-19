# https:\_\_weaviate.io_developers_weaviate_modules_retriever-vectorizer-modules_img2vec-neural#nearimage

The img2vec-neural module enables Weaviate to obtain vectors locally using a resnet50 model. It encapsulates the model in a Docker container, which allows independent scaling on GPU-enabled hardware. For new projects, we recommend using the multi2vec -clip module instead. This uses CLIP models, which uses a more modern model architecture.
