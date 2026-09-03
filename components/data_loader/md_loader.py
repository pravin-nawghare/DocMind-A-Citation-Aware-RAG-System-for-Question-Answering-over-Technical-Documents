import json
from pathlib import Path
from config import setting
from components.utils import initiate_tokenizer
from langchain_docling import DoclingLoader



json_storage_path = Path("output_md.json") 
data_storage_directory = Path("storage")
file_path = Path("data\\Gen AI Project readme structure.md")
tokenizer_model = setting.TOKENIZER_MODEL

def _docling_md_loader(md_file_path: Path):
    """
    Load all Markdown files from the specified directory and return docling loader object.
    
    Args:
        md_file_path (Path): The path to the Markdown file to load.
    """

    loader = DoclingLoader(
                file_path=str(md_file_path),
                chunker=initiate_tokenizer(tokenizer_model))#, max_tokens=512)
    print("md loader object created successfully")
    return loader

def  _load_md_into_json(document_loader, json_file_path: Path):
    """
    Load documents from the document loader and save them into a JSON file.

    Args:
        document_loader: The document loader object to load documents from.
        json_file_path (str): The path to the JSON file where the documents will be saved.
    """
    try:
        md_loader = document_loader
        docs_lazy = md_loader.lazy_load()
        documents = []

        for doc in docs_lazy:
            # to add custom metadata
            # doc.metadata["department"] = "finance"
            documents.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
            })

        print("markdown data appended to documents list successfully")
        # Save the documents to a JSON file
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(documents, json_file, ensure_ascii=False, indent=4)

        print(f"Documents saved to {json_file_path}")

    except Exception as e:
        print(f"An error occurred while loading markdown documents into JSON: {e}")
        raise

def load_md_files():
    """
    Load Markdown files from the specified path and save them into a JSON file.

    Args:
        md_file_path (Path): The path to the Markdown file to load.
        json_file_path (Path): The path to the JSON file where the documents will be saved.
    """
    print("inside load_md_files function")
    try:
        # Create a docling loader for the Markdown files
        document_loader = _docling_md_loader(file_path)

        # Load documents into JSON
        _load_md_into_json(document_loader, data_storage_directory / json_storage_path)

    except Exception as e:
        print(f"An error occurred while loading Markdown files: {e}")
        raise

    
         