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

website_content_collection = db["website_content"]
portal_services_collection = db["portal_services"]
portal_departments_collection = db["portal_departments"]