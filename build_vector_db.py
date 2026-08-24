import os
import shutil

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DOCS_FOLDER = "docs"
VECTOR_STORE_FOLDER = "vector_store"
COLLECTION_NAME = "ieso_documents"


def build_vector_database():
    if not os.path.exists(DOCS_FOLDER):
        raise FileNotFoundError("The docs folder does not exist.")

    pdf_files = [
        file for file in os.listdir(DOCS_FOLDER)
        if file.lower().endswith(".pdf")
    ]

    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the docs folder.")

    print(f"Found {len(pdf_files)} PDF files:")
    for file in pdf_files:
        print(f"- {file}")

    if os.path.exists(VECTOR_STORE_FOLDER):
        print("\nOld vector_store folder found. Deleting it...")
        shutil.rmtree(VECTOR_STORE_FOLDER)

    print("\nLoading PDFs...")
    loader = PyPDFDirectoryLoader(DOCS_FOLDER)
    documents = loader.load()

    print(f"Loaded {len(documents)} document pages.")

    print("\nSplitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} text chunks.")

    print("\nCreating local embeddings and saving to Chroma...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_STORE_FOLDER
    )

    print("\nVector database created successfully.")
    print(f"Saved to: {VECTOR_STORE_FOLDER}/")


if __name__ == "__main__":
    build_vector_database()