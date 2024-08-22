from langchain_core.messages import BaseMessage
import json
from typing import Any, TypedDict

MessageCls =  str | BaseMessage | list[str] | tuple[str, str] | str | dict[str, Any]
class MessageDict(TypedDict):
    type: str
    content: str

def serialize_message(message: MessageCls) -> MessageDict:
    if isinstance(message, str):
        # Handle string type
        return {
            "type": "system",
            "content": message
        }
    elif isinstance(message, BaseMessage):
        # Handle BaseMessage type
        return {
            "type": message.type,
            "content": message.content
        }
    elif isinstance(message, list) or isinstance(message, tuple):
        # Handle list of strings
        return {
            "type": message[0],
            "content": message[1]
        }
    elif isinstance(message, dict):
        key, value = list(message.items())[0]
        return {
            "type": key,
            "content": str(value)  # Convert dict to a JSON string for content
        }
    else:
        raise ValueError(f"Unsupported message type: {type(message)}")

def serialize_message_to_str(message: MessageCls) -> str:
    json_message = serialize_message(message)
    return json.dumps(json_message)

def deserialize_message(message: MessageDict) -> MessageCls:
    return message["type"], message["content"]

def deserialize_message_from_str(message: str) -> MessageCls:
    return deserialize_message(json.loads(message))