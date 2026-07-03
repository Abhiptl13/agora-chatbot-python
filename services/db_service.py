import re
from bson import ObjectId
from bson.errors import InvalidId

from mongo_db import (
    users_collection,
    knowledge_collection,
    documents_collection,
    appointments_collection,
    conversations_collection
)


DEFAULT_LIMIT = 50
MAX_LIMIT = 100


def normalize_limit(limit):
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = DEFAULT_LIMIT

    if limit <= 0:
        return DEFAULT_LIMIT

    return min(limit, MAX_LIMIT)


def get_object_id_or_none(value):
    try:
        return ObjectId(str(value))
    except (InvalidId, TypeError, ValueError):
        return None


def make_json_safe(value):
    if isinstance(value, ObjectId):
        return str(value)

    if isinstance(value, list):
        return [make_json_safe(item) for item in value]

    if isinstance(value, dict):
        return {
            key: make_json_safe(item)
            for key, item in value.items()
        }

    return value


def serialize_items(items):
    return [make_json_safe(item) for item in items]


def build_role_filter(role=None):
    if not role:
        return {}

    role_lower = str(role).lower().strip()

    if role_lower in ["admin", "administrator"]:
        return {}

    return {
        "audience": {
            "$in": [
                role,
                role_lower,
                role_lower.capitalize(),
                "all",
                "general"
            ]
        }
    }


def build_safe_regex_query(query, fields):
    if not query:
        return {}

    safe_query = re.escape(str(query).strip())

    if not safe_query:
        return {}

    return {
        "$or": [
            {
                field: {
                    "$regex": safe_query,
                    "$options": "i"
                }
            }
            for field in fields
        ]
    }


def combine_filters(filter_one, filter_two):
    if filter_one and filter_two:
        return {
            "$and": [
                filter_one,
                filter_two
            ]
        }

    if filter_one:
        return filter_one

    if filter_two:
        return filter_two

    return {}


def get_users(limit=DEFAULT_LIMIT):
    limit = normalize_limit(limit)

    results = users_collection.find(
        {},
        {
            "password": 0
        }
    ).limit(limit)

    return serialize_items(list(results))


def get_user_by_email(email):
    if not email:
        return None

    user = users_collection.find_one(
        {
            "email": email
        },
        {
            "password": 0
        }
    )

    if not user:
        return None

    return make_json_safe(user)


def get_documents(role=None, query=None, limit=DEFAULT_LIMIT):
    limit = normalize_limit(limit)

    role_filter = build_role_filter(role)

    search_filter = build_safe_regex_query(
        query,
        [
            "title",
            "category",
            "summary",
            "type",
            "original_file_name",
            "file_name",
            "content_text",
            "description"
        ]
    )

    mongo_query = combine_filters(role_filter, search_filter)

    results = documents_collection.find(
        mongo_query
    ).sort(
        "uploaded_at",
        -1
    ).limit(limit)

    return serialize_items(list(results))


def get_document_by_id(document_id):
    object_id = get_object_id_or_none(document_id)

    if not object_id:
        return None

    document = documents_collection.find_one({
        "_id": object_id
    })

    if not document:
        return None

    return make_json_safe(document)


def get_knowledge(role=None, query=None, limit=DEFAULT_LIMIT):
    limit = normalize_limit(limit)

    role_filter = build_role_filter(role)

    search_filter = build_safe_regex_query(
        query,
        [
            "title",
            "category",
            "keywords",
            "answer",
            "summary",
            "text",
            "content",
            "description"
        ]
    )

    mongo_query = combine_filters(role_filter, search_filter)

    results = knowledge_collection.find(
        mongo_query
    ).sort(
        "title",
        1
    ).limit(limit)

    return serialize_items(list(results))


def get_knowledge_by_id(knowledge_id):
    object_id = get_object_id_or_none(knowledge_id)

    if not object_id:
        return None

    knowledge = knowledge_collection.find_one({
        "_id": object_id
    })

    if not knowledge:
        return None

    return make_json_safe(knowledge)


def get_user_appointments(user_email, limit=DEFAULT_LIMIT):
    if not user_email:
        return []

    limit = normalize_limit(limit)

    results = appointments_collection.find({
        "user": user_email
    }).sort(
        "created_at",
        -1
    ).limit(limit)

    return serialize_items(list(results))


def get_all_appointments(status=None, limit=DEFAULT_LIMIT):
    limit = normalize_limit(limit)

    mongo_query = {}

    if status:
        mongo_query["status"] = status

    results = appointments_collection.find(
        mongo_query
    ).sort(
        "created_at",
        -1
    ).limit(limit)

    return serialize_items(list(results))


def get_appointment_by_id(appointment_id):
    object_id = get_object_id_or_none(appointment_id)

    if not object_id:
        return None

    appointment = appointments_collection.find_one({
        "_id": object_id
    })

    if not appointment:
        return None

    return make_json_safe(appointment)


def get_user_conversations(user_email, limit=DEFAULT_LIMIT):
    if not user_email:
        return []

    limit = normalize_limit(limit)

    results = conversations_collection.find({
        "user": user_email
    }).sort(
        "timestamp",
        -1
    ).limit(limit)

    return serialize_items(list(results))


def get_recent_conversations(limit=DEFAULT_LIMIT):
    limit = normalize_limit(limit)

    results = conversations_collection.find(
        {}
    ).sort(
        "timestamp",
        -1
    ).limit(limit)

    return serialize_items(list(results))