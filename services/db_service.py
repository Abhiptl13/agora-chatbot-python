from mongo_db import (
    users_collection,
    knowledge_collection,
    documents_collection,
    appointments_collection,
    conversations_collection
)

def get_users():
    return list(users_collection.find({}))

def get_documents():
    return list(documents_collection.find({}))

def get_knowledge():
    return list(knowledge_collection.find({}))