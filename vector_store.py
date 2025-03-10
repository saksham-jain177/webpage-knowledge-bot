import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["USER_AGENT"] = "BrainloxChatbot/1.0"
from dotenv import load_dotenv
import tensorflow as tf
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from data_loader import load_data

# Load environment variables from .env file
load_dotenv()

tf.get_logger().setLevel('ERROR')

def create_vector_store(documents):    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")    
    vector_store = FAISS.from_documents(documents, embeddings)    
    vector_store.save_local("faiss_index")
    print("Vector store created and saved.")

if __name__ == "__main__":
    url = "https://brainlox.com/courses/category/technical"
    documents = load_data(url)
    create_vector_store(documents)