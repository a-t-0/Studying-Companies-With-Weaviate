FROM semitechnologies/sum-transformers:custom
RUN chmod +x ./download.py
RUN MODEL_NAME=google/pegasus-pubmed ./download.py
