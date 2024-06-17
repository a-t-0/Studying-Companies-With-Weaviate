# https:\_\_weaviate.io_papers_radit

When you prompt an LLM, RAG supplies relevant documents. A separate retrieval model computes the probability of each text chunk being relevant. Fine-tuning the LLM and retrieval model together can improve performance without requiring extensive data processing.Authors from Meta fine-tuned Llama 2 (65B parameters) and DRAGON+ a retriever, to create RA-DIT 65B.
