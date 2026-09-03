from pathlib import Path
from config import setting
from components.file_loader.load_files import load_files_from_directory
from components.data_loader.pdf_loader import load_pdf_files
from components.data_loader.md_loader import load_md_files

hf_token = setting.HF_TOKEN
# directory_file_path = Path("data")

# files = load_files_from_directory(directory_file_path)
# print(f"Loaded {len(files)} files from the directory.")
# for i, file_path in enumerate(files):
#     print(f"{i + 1}: {file_path}")

# load_pdf_files(folder_name="test")
# load_md_files()