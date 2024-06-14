# Load model directly
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# pipe = pipeline("summarization", model="facebook/bart-large-cnn")


tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
