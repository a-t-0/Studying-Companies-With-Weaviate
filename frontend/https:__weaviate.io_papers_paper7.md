# https:\_\_weaviate.io_papers_paper7

Researchers at MicrosoftAI propose "unlearning" or "un-training" as a three-step process. First they finetune a model to always respond with some reference to the information they want to later erase. This "reinforced model" becomes a specialist in the information we eventually want to unlearn. This step is used to identify which tokens should be targeted in the unlearning step.
