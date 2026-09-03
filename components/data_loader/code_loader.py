import json
from pathlib import Path
from config import setting
from components.utils import initiate_tokenizer
from langchain_community.document_loaders import PythonLoader, NotebookLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language



py_storage_path = Path("output_py.json") 
ipynb_storage_path = Path("output_ipynb.json")
data_storage_directory = Path("storage")
file_path = Path()


def _python_loader(py_file_path: Path):
    """
    Load all Python/Notebook files from the specified directory and return docling loader object.
    
    Args:
        py_file_path (Path): The path to the Python file to load.
    """
    file_extension = py_file_path.suffix.lower()
    if file_extension == ".py":
        loader = PythonLoader(str(py_file_path))
    elif file_extension == ".ipynb":
        loader = NotebookLoader(str(py_file_path),
                                include_outputs=False)

# If you're building a code RAG system, though, I would go one step further and preserve notebook metadata such as 
# cell number, cell type, execution count, and source file in the Document.metadata. That makes retrieval and 
# citations substantially better.

    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")
    print("Python/Notebook loader object created successfully")
    return loader

def  _load_py_into_json(document_loader, json_file_path: Path):
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

        splitter = RecursiveCharacterTextSplitter.from_language(
                                        language=Language.PYTHON,
                                        chunk_size=1000,
                                        chunk_overlap=100,
                                    )

        chunks = splitter.split_documents(documents)

        print("code data appended to documents list successfully")
        # Save the documents to a JSON file
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(chunks, json_file, ensure_ascii=False, indent=4)

        print(f"Documents saved to {json_file_path}")

    except Exception as e:
        print(f"An error occurred while loading code documents into JSON: {e}")
        raise

def load_py_files():
    """
    Load Python/Notebook files from the specified path and save them into a JSON file.

    Args:
        py_file_path (Path): The path to the Python/Notebook file to load.
        json_file_path (Path): The path to the JSON file where the documents will be saved.
    """
    print("inside load_py_files function")
    try:
        # Create a docling loader for the Python/Notebook files
        document_loader = _python_loader(file_path)

        file_extension = file_path.suffix.lower()

        # Load documents into JSON
        if file_extension == ".py":
            _load_py_into_json(document_loader, data_storage_directory / py_storage_path)
        elif file_extension == ".ipynb":
            _load_py_into_json(document_loader, data_storage_directory / ipynb_storage_path)

    except Exception as e:
        print(f"An error occurred while loading Python/Notebook files: {e}")
        raise

    
         