import os
os.environ["USER_AGENT"] = "BrainloxChatbot/1.0"

from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

def load_data(url):
    loader = WebBaseLoader(web_path=url)
    documents = loader.load()
    return documents

if __name__ == "__main__":
    url = "https://brainlox.com/courses/category/technical"
    documents = load_data(url)
    print(f"Loaded {len(documents)} documents.")