from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
import pickle

INDEX_DIR = "data/faiss_index"


class TfidfEmbeddings(Embeddings):
    def embed_documents(self, texts):
        raise RuntimeError("embed_documents should not be called during retrieval")

    def embed_query(self, text):
        with open(f"{INDEX_DIR}/vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)

        return vectorizer.transform([text]).toarray()[0].tolist()


def load_vectorstore():
    embeddings = TfidfEmbeddings()

    try:
        return FAISS.load_local(
            INDEX_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )
    except TypeError:
        return FAISS.load_local(
            INDEX_DIR,
            embeddings
        )


def retrieve(query: str, k: int = 5):
    db = load_vectorstore()
    return db.similarity_search(query, k=k)


if __name__ == "__main__":
    query = "How should customer support handle unhappy customers?"
    docs = retrieve(query)

    print(f"Retrieved {len(docs)} documents:\n")
    for i, doc in enumerate(docs, 1):
        print(f"[{i}] {doc.page_content[:300]}...\n")
