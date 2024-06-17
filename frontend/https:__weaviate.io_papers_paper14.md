# https:\_\_weaviate.io_papers_paper14

Work from Microsoft uses synthetic data + LLMs as embedding models to achieve SOTA on the MTEB benchmark. They generate a multilingual synthetic retrieval dataset using GPT-4 which includes {queries, positive matches, hard negatives}. They use this synthetic dataset along with 13 other public datasets and embed the queries & negatives using the last layer vectors of Mistral-7B.
