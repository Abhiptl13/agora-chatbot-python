from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["agora_chatbot_db"]

users_collection = db["users"]
knowledge_collection = db["knowledge_base"]
documents_collection = db["documents"]
appointments_collection = db["appointments"]
conversations_collection = db["conversations"]