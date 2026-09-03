from config import setting
from transformers import AutoTokenizer
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer


hf_token = setting.HF_TOKEN

def initiate_tokenizer(docling_tokenizer: str):
    """
    This function initializes a tokenizer using the HuggingFace library and returns a HybridChunker object. 

    Args:
        chunker: HybridChunker object that will be used to chunk the documents.
    """
    tokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained(docling_tokenizer),
        max_tokens=512
    )

    chunker = HybridChunker(tokenizer=tokenizer)
    return chunker