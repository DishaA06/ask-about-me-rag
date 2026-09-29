import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.config import DATA_DIR, VECTORSTORE_DIR, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL
import glob

def load_documents():
    docs = []

    resumes_dir = os.path.join(DATA_DIR, "resumes")
    if os.path.exists(resumes_dir):
        pdf_files = glob.glob(os.path.join(resumes_dir, "*.pdf"))
        if pdf_files:
            for pdf_path in pdf_files:
                docs.extend(PyPDFLoader(pdf_path).load())
        else:
            print("No resume PDFs found, skipping.")
    else:
        print("No resumes folder found, skipping.")

    projects_dir = os.path.join(DATA_DIR, "projects")
    if os.path.exists(projects_dir) and os.listdir(projects_dir):
        projects_loader = DirectoryLoader(projects_dir, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        docs.extend(projects_loader.load())
    else:
        print("No project files found, skipping.")

    certs_dir = os.path.join(DATA_DIR, "certs")
    if os.path.exists(certs_dir) and os.listdir(certs_dir):
        certs_loader = DirectoryLoader(certs_dir, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        docs.extend(certs_loader.load())
    else:
        print("No cert files found, skipping.")

    return docs


def build_index():
    print("Loading documents...")
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.")

    profile_dir = os.path.join(DATA_DIR, "profile")
    if os.path.isdir(profile_dir):
        docs.extend(DirectoryLoader(profile_dir, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}).load())

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    for c in chunks:  # label each chunk with its origin to help retrieval
        name = os.path.basename(c.metadata.get("source", "")).replace(".pdf", "").replace(".md", "").replace(".txt", "")
        c.page_content = f"[{name}]\n{c.page_content}"
    print(f"Created {len(chunks)} chunks.")

    print("Embedding and building FAISS index (this downloads a small local model the first time)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    vectorstore.save_local(VECTORSTORE_DIR)
    print(f"Index saved to '{VECTORSTORE_DIR}'.")


if __name__ == "__main__":
    build_index()