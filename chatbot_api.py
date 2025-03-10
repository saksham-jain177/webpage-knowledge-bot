import os
import logging
import requests
from datetime import datetime
import pytz
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
logging.getLogger('tensorflow').setLevel(logging.ERROR)
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

llm = ChatOpenAI(
    model_name="google/gemini-2.0-flash-lite-preview-02-05:free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.1,
    max_tokens=100
)

# Updated prompt with time estimation
prompt_template = PromptTemplate(
    input_variables=["question", "context", "user_timezone"],
    template="Answer in 1-2 concise sentences. For technical course questions, extract info from the context; for time-related queries, use the user’s timezone ({user_timezone}); for duration questions, estimate time (assume 1 lesson = 1 hour unless specified); otherwise, respond as a helpful AI chatbot.\nContext: {context}\nQuestion: {question}\nAnswer:"
)

def truncate_text(text, max_tokens=400):
    max_chars = max_tokens * 4
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text

def get_user_timezone(ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=5)
        data = response.json()
        return data.get("timezone", "UTC")
    except Exception as e:
        logger.error(f"Error fetching timezone: {e}")
        return "UTC"

def get_current_time_in_timezone(timezone_str):
    try:
        tz = pytz.timezone(timezone_str)
        return datetime.now(tz).strftime("%I:%M %p %Z on %B %d, %Y")
    except Exception as e:
        logger.error(f"Error with timezone {timezone_str}: {e}")
        return datetime.now(pytz.UTC).strftime("%I:%M %p UTC on %B %d, %Y")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    client_ip = request.remote_addr
    logger.debug(f"Received query: {query} from IP: {client_ip}")
    
    try:
        user_timezone = get_user_timezone(client_ip)
        current_time = get_current_time_in_timezone(user_timezone)

        if "course" in query.lower() or "technical" in query.lower():
            retriever = vector_store.as_retriever(search_kwargs={"k": 1})
            docs = retriever.invoke(query)
            context = " ".join([doc.page_content for doc in docs])
        elif "time" in query.lower():
            if "ist" in query.lower():
                context = f"The current time is {get_current_time_in_timezone('Asia/Kolkata')}."
            else:
                context = f"The current time is {current_time}."
        else:
            context = "I am a chatbot designed to assist with information about technical courses and general queries."

        truncated_context = truncate_text(context)
        logger.debug(f"Truncated context: {truncated_context}")
        
        prompt = prompt_template.format(
            question=query,
            context=truncated_context,
            user_timezone=user_timezone
        )
        logger.debug(f"Full prompt: {prompt}")
        
        answer = llm.invoke(prompt).content.strip()
        logger.debug(f"Answer: {answer}")
        
        return jsonify({"response": answer})
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)