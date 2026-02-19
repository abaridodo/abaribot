import os
from typing import List, Optional
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

# LangChain document loaders
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredURLLoader
)
load_dotenv()
class VectorDBPopulator:
    """
    A universal loader and populator for vector databases.
    Supports .txt, .pdf, .docx, and web pages.
    """

    def __init__(self, index_name: str, embedding_model: str = "text-embedding-ada-002"):
        load_dotenv()
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pinecone.Index(index_name)
        self.embedding_model = embedding_model

    # -----------------------------
    # Document Loading
    # -----------------------------
    def load_document(self, file_path_or_url: str) -> str:
        """
        Load text content from a document (supports txt, pdf, docx, and URLs).
        """
        if file_path_or_url.startswith("http"):
            loader = UnstructuredURLLoader(urls=[file_path_or_url])
        elif file_path_or_url.endswith(".pdf"):
            loader = PyPDFLoader(file_path_or_url)
        elif file_path_or_url.endswith(".docx"):
            loader = Docx2txtLoader(file_path_or_url)
        elif file_path_or_url.endswith(".txt"):
            loader = TextLoader(file_path_or_url)
        else:
            raise ValueError(f"Unsupported file type: {file_path_or_url}")

        documents = loader.load()
        return "\n".join([doc.page_content for doc in documents])

    # -----------------------------
    # Chunking
    # -----------------------------
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks for embedding.
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk.strip())
            start += chunk_size - overlap
        return [c for c in chunks if c]

    # -----------------------------
    # Embedding Creation
    # -----------------------------
    def _get_embedding(self, text: str) -> List[float]:
        response = self.openai_client.embeddings.create(
            model=self.embedding_model, input=text
        )
        return response.data[0].embedding

    # -----------------------------
    # Database Insertion
    # -----------------------------
    def upsert_chunk(self, chunk: str, doc_id: str):
        try:
            embedding = self._get_embedding(chunk)
            self.index.upsert([
                {
                    "id": doc_id,
                    "values": embedding,
                    "metadata": {"content": chunk}
                }
            ])
            print(f"✅ Inserted chunk: {doc_id}")
        except Exception as e:
            print(f"❌ Error inserting {doc_id}: {e}")

    # -----------------------------
    # High-Level Populate
    # -----------------------------
    def populate(
        self,
        file_path_or_url: str,
        prefix: Optional[str] = None,
        chunk_size: int = 1000,
        overlap: int = 100,
    ):
        """
        Load a document (or URL), split it into chunks, embed, and store in Pinecone.
        """
        text = self.load_document(file_path_or_url)
        chunks = self.chunk_text(text, chunk_size, overlap)
        prefix = prefix or os.path.splitext(os.path.basename(file_path_or_url))[0]

        for i, chunk in enumerate(chunks):
            doc_id = f"{prefix}_{i}"
            self.upsert_chunk(chunk, doc_id)

        print(f"\n📘 Finished populating {len(chunks)} chunks from {file_path_or_url}")

if __name__ == "__main__":
    populator = VectorDBPopulator(index_name="abaribot")

    # populator.populate("docs/abari_genai.txt", prefix="abari_txt")

    # # ✅ PDF
    populator.populate("docs/abari.pdf", prefix="ai_pdf")