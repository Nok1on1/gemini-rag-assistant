from bson.objectid import ObjectId
from langchain.schema import AIMessage, HumanMessage


def convert_mongo_history_to_langchain(history_data):
    messages = []
    for item in history_data:
        role = item.get("role")
        text = item.get("parts", [{}])[0].get("text", "")

        if role == "user":
            messages.append(HumanMessage(content=text))
        elif role == "model":
            messages.append(AIMessage(content=text))
    return messages


def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_objectid(i) for i in obj]
    return obj
