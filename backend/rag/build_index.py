import os

from langchain_text_splitters import CharacterTextSplitter

from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(BASE_DIR, "books")
DB_DIR = os.path.join(BASE_DIR, "db")

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def build_index(mentor_id: str):
    book_path = os.path.join(BOOKS_DIR, f"{mentor_id}.txt")
    persist_dir = os.path.join(DB_DIR, f"{mentor_id}_chroma")

    if not os.path.exists(book_path):
        raise FileNotFoundError(f"No book found for {mentor_id}")

    loader = TextLoader(book_path, encoding="utf-8")
    docs = loader.load()

    splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=persist_dir
    )

    print(f"✅ Vector DB built for {mentor_id}")

if __name__ == "__main__":
    for mentor in ["krishna", "rama", "bahubali"]:
        build_index(mentor)
