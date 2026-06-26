import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConfigurationError


# -----------------------------
# MONGODB CONFIGURATION
# -----------------------------

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is missing. Please add it to your environment variables.")

client = MongoClient(MONGO_URI)

database_name = (
    os.getenv("MONGO_DB_NAME")
    or os.getenv("MONGO_DATABASE")
    or "agora_chatbot_db"
)

try:
    db = client.get_default_database()
except ConfigurationError:
    db = client[database_name]


# -----------------------------
# COLLECTIONS
# -----------------------------

users_collection = db["users"]
knowledge_collection = db["knowledge_base"]
documents_collection = db["documents"]
appointments_collection = db["appointments"]
conversations_collection = db["conversations"]

website_content_collection = db["website_content"]
portal_services_collection = db["portal_services"]
portal_departments_collection = db["portal_departments"]