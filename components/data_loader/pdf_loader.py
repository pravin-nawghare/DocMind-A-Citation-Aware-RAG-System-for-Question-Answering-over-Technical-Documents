import os
import json
from pathlib import Path
from xml.parsers.expat import model
from config import setting
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from transformers import AutoTokenizer
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from components.utils import initiate_tokenizer

json_storage_path = Path("output.json") 
data_storage_directory = Path("storage")
file_path = Path("data\\Hands-On_Machine_Learning_with_Scikit-Learn,_Keras_and_TensorFlow.pdf")
hf_token = setting.HF_TOKEN
tokenizer_model = setting.TOKENIZER_MODEL
# "BAAI/bge-m3" with max_tokens=1024 for context window

def _docling_pdf_loader(pdf_file_path: Path):
    """
    Load all PDF files from the specified directory and return unstructured loader object.
    
    Args:
        pdf_file_path (Path): The path to the PDF file to load.
    """

    tokenizer = HuggingFaceTokenizer(
                    tokenizer=AutoTokenizer.from_pretrained(tokenizer_model), 
                    max_tokens=512)

    loader = DoclingLoader(
                file_path=str(pdf_file_path),
                chunker=HybridChunker(tokenizer=tokenizer), max_tokens=512)
    print("pdf loader object created successfully")
    return loader

#---------
# For a RAG pipeline, it's better to process each chunk immediately:
# for doc in pdf_loader.lazy_load():
#     vectorstore.add_documents([doc])
#---------------

def _load_into_json(document_loader, json_file_path: Path):
    """
    Load documents from the document loader and save them into a JSON file.

    Args:
        document_loader: The document loader object to load documents from.
        json_file_path (str): The path to the JSON file where the documents will be saved.
    """
    try:
        pdf_loader = document_loader
        docs_lazy = pdf_loader.lazy_load()
        documents = []

        for doc in docs_lazy:
            # to add custom metadata
            # doc.metadata["department"] = "finance"
            documents.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
            })
        print("pdf data appended to documents list successfully")

        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(documents, f, ensure_ascii=False, indent=2) 
        print("pdf data dumped into json file successfully:", json_file_path)

    except Exception as e:
        print(f"An error occurred while parsing PDF files: {str(e)}")
        raise


def load_pdf_files(folder_name: str):
    try:
        print("inside load_pdf_files function")
        if folder_name in os.listdir(data_storage_directory):
            print("folder already exists in storage directory")
            print("loading pdf loader")
            pdf_loader = _docling_pdf_loader(file_path)
            print("loading pdf data into json file")
            _load_into_json(pdf_loader, data_storage_directory / folder_name/ json_storage_path)
        else:
            os.makedirs(data_storage_directory / folder_name, exist_ok=True)
            print("folder created successfully")
            print("loading pdf loader")
            pdf_loader = _docling_pdf_loader(file_path)           
            print("loading pdf data into json file")
            _load_into_json(pdf_loader, data_storage_directory / folder_name/ json_storage_path)
    except Exception as e:
        print(f"An error occurred while loading PDF files into {folder_name}: {str(e)}")
        raise