import dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS 
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

def set_up():
    dotenv.load_dotenv()

class LLMService:
    def __init__():
        pass
    
    def _open_ai(model_name="gpt-4", temperature=0.7):
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
        return llm
    def _anthropic_llm(self, ):
        pass
    def _custom_llm(self, ):
        pass
    
    def build_rag(self, llm, vectorstore):
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            memory=memory
            )
def docs_splitter(docs_path='/content/RAG/abari.txt'):
    loader = TextLoader(file_path=docs_path, encoding="utf-8")
    data = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    data = text_splitter.split_documents(data)
    return data

def docs_to_vectorstores(data):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(data, embedding=embeddings)
    return vectorstore

def get_gpt():
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    return llm, memory

def rag_system(llm, memory, vectorstore):
    conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            memory=memory
            )
    return conversation_chain

def chat_with_abari(docs_path):
    set_up()
    llm, memory = get_gpt()
    data = docs_splitter(docs_path=docs_path)
    vectorstore = docs_to_vectorstores(data)
    conversation_chain = rag_system(llm, memory, vectorstore)
    return conversation_chain

# chat = rag_system = chat_with_abari('docs/abari.txt')
if __name__=="__main__":
    # rag_system = chat_with_abari('docs/abari.txt')
    # while True:
    #     query = input("You: ")
    #     result = rag_system.invoke({"question": query})
    #     answer = result["answer"]
    #     print("Abari assistant: " + answer)
    data = docs_splitter("docs/abari.txt")
    print(type(data))
        