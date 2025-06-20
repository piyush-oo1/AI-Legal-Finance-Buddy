# agents/vector_agent.py

import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader, TextLoader

class VectorAgent:
    DB_PATH = "./vector_db"
    EMBEDDING_MODEL = OpenAIEmbeddings()

    @staticmethod
    def _get_store():
        return Chroma(persist_directory=VectorAgent.DB_PATH, embedding_function=VectorAgent.EMBEDDING_MODEL)

    @staticmethod
    def _make_doc(doc_type, terms, draft, summary, feedback, pdf_url):
        metadata = {
            "doc_type": doc_type,
            "terms": terms,
            "draft": draft,
            "summary": summary,
            "feedback": feedback,
            "pdf_url": pdf_url
        }
        content = f"{doc_type}\n\n{terms}\n\n{draft}\n\n{summary}\n\n{feedback}"
        return Document(page_content=content, metadata=metadata)

    @staticmethod
    def store_document(doc_type, terms, draft, summary, feedback, pdf_url):
        doc = VectorAgent._make_doc(doc_type, terms, draft, summary, feedback, pdf_url)
        store = VectorAgent._get_store()
        store.add_documents([doc])
        store.persist()

    @staticmethod
    def search_existing(doc_type, terms, threshold=0.9):
        store = VectorAgent._get_store()
        query = f"{doc_type}\n\n{terms}"
        results = store.similarity_search_with_score(query, k=1)

        if results and results[0][1] >= threshold:
            metadata = results[0][0].metadata
            return {
                "draft": metadata.get("draft", ""),
                "summary": metadata.get("summary", ""),
                "feedback": metadata.get("feedback", ""),
                "pdf_url": metadata.get("pdf_url", "")
            }
        return None

    @staticmethod
    def _load_document(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            loader = PyMuPDFLoader(file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        return loader.load()

    @staticmethod
    def ingest_document(path, doc_type):
        try:
            print(f"[INFO] Loading document: {path}")
            docs = VectorAgent._load_document(path)
            print(f"[INFO] Loaded {len(docs)} document(s)")
            for doc in docs:
                doc.metadata["doc_type"] = doc_type

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(docs)
            print(f"[INFO] Split into {len(chunks)} chunk(s)")

            db = Chroma.from_documents(
                documents=chunks,
                embedding=VectorAgent.EMBEDDING_MODEL,
                persist_directory=VectorAgent.DB_PATH
            )
            db.persist()
            print(f"[✅] Ingested and saved to Chroma Vector DB from: {path}")
        except Exception as e:
            print(f"[ERROR] Failed to ingest document: {e}")
