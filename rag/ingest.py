import os
import pickle
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = "data/docs"
INDEX_DIR = "data/faiss_index"


class TfidfEmbeddings(Embeddings):
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.fitted = False

    def embed_documents(self, texts):
        vectors = self.vectorizer.fit_transform(texts)
        self.fitted = True

        os.makedirs(INDEX_DIR, exist_ok=True)
        with open(f"{INDEX_DIR}/vectorizer.pkl", "wb") as f:
            pickle.dump(self.vectorizer, f)

        return vectors.toarray().tolist()

    def embed_query(self, text):
        with open(f"{INDEX_DIR}/vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)

        return vectorizer.transform([text]).toarray()[0].tolist()


def load_documents():
    documents = []
    for file in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, file)

        if file.endswith(".pdf"):
            documents.extend(PyPDFLoader(path).load())
        elif file.endswith(".txt"):
            documents.extend(TextLoader(path).load())

    return documents


def ingest():
    print("Loading documents...")
    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    texts = [doc.page_content for doc in chunks]
    embeddings = TfidfEmbeddings()

    db = FAISS.from_texts(texts, embeddings)
    db.save_local(INDEX_DIR)

    print("✅ FAISS index created using TF‑IDF embeddings")


if __name__ == "__main__":
    ingest()
