import os
from dotenv import load_dotenv

import openai
from pinecone import Pinecone

load_dotenv()
# OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("abaribot")

def query(user_question):

    try:
        # Generate embeddings for the question
        question_embedding_response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=user_question
        )
        question_embedding = question_embedding_response.data[0].embedding

        # Search the vector database for relevant content
        search_results = index.query(
            vector=question_embedding,
            top_k=1,
            include_metadata=True
        )

        if not search_results['matches']:
            return "No relevant content found in the database."

        # Retrieve the most relevant content
        relevant_content = search_results['matches'][0]['metadata']['content']
        # Generate an answer using the relevant content
        completion_response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": relevant_content},
                {"role": "user", "content": user_question } ],
            max_tokens=200
        )

        answer = completion_response.choices[0].message
        return answer.content
    except Exception as e:
        return f"Error querying the database: {str(e)}"

if __name__ == "__main__":
    while True:
        question = input("You: ")
        if question.lower().strip() == "quit":
            break
        answer = query(question)
        print(f"Answer: {answer}")