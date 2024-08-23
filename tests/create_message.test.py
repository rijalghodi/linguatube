from app.service import insert_message
from packages.shared import SupabaseClient
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from packages import serialize_message_to_str

if __name__ == '__main__':
    load_dotenv()

    message = HumanMessage(content="Hello")

    message_str = serialize_message_to_str(message)

    client = SupabaseClient()

    res = insert_message(client, message_str, video_id="247e3ca7-e281-4012-a6cc-7208e3fcb223")
    print(res)