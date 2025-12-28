 import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "rag", "db")

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def get_retriever(mentor_id: str):
    persist_dir = os.path.join(DB_DIR,
