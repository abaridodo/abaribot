import os
from dotenv import load_dotenv
from typing import List

import openai
from pinecone import Pinecone

load_dotenv()
# OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("abaribot")

def chunk_docs(file_path: str, chunk_strat=None, chunk_size:int=1000, overlap:int=100)-> List[str]:
    with open(file_path) as fp:
        content = fp.read()
    chunks = []
    num_chunks = len(content)//chunk_size
    for i in range(num_chunks, overlap):
        chunk = content[i: i+ chunk_size]
        chunks.append(chunk)
    return chunks

def populate_chunk(chunk:List[str], doc_id:int):
    try:
        embedding_response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=chunk
        )
        content_embedding = embedding_response.data[0].embedding

        index.upsert([{
            "id": doc_id,
            "values": content_embedding,
            "metadata": {"content": chunk}
        }])

        print(f"Successfully populated vector database with document ID: {doc_id}")
    except Exception as e:
        print(f"Error populating vector database: {str(e)}")
        
def populate(file_path:str, doc_id:int):
    """
    Populate the vector database with embeddings from a text file.

    Args:
        file_path (str): Path to the text file.
        doc_id (str): Unique identifier for the document in the vector database.
    """
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Generate embeddings for the content
        embedding_response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=content
        )
        content_embedding = embedding_response.data[0].embedding

        # Store the embeddings in Pinecone
        index.upsert([{
            "id": doc_id,
            "values": content_embedding,
            "metadata": {"content": content}
        }])

        print(f"Successfully populated vector database with document ID: {doc_id}")
    except Exception as e:
        print(f"Error populating vector database: {str(e)}")

# Example Usage
if __name__ == "__main__":
    # populate("abari.txt", doc_id="doc-1")
    chunks = chunk_docs('docs/abari_genai.txt')
    for i, chunk in enumerate(chunks):
        doc_id = f"abari_{i}"
        populate_chunk(chunk, doc_id)
        print(f"{doc_id} is inserted")
