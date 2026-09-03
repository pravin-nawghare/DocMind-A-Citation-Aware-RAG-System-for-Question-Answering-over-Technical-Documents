from dotenv import load_dotenv
import os


load_dotenv()

class Settings():
    # Api keys
    GEMINI_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    HF_TOKEN: str = os.getenv("HF_TOKEN")

    # LLM models
    GEMINI_MODEL= "gemini-2.5-flash"
    GEMINI_FALLBACK_MODEL = ""
    GROQ_MODEL = "llama-3.3-70b-versatile"
    GROQ_FALLBACK_MODEL = ""

    TOKENIZER_MODEL = "BAAI/bge-small-en-v1.5"
    # Run the fastapi server
    APP_PORT = os.getenv("APP_PORT")
    APP_HOST = os.getenv("APP_HOST")



setting = Settings()