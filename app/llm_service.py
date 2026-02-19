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