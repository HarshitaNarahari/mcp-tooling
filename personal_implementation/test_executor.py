import asyncio
from a2a.types import Part, TextPart, Message
from a2a.client import ClientFactory, ClientConfig
from agent_cards import agent1_card
import uuid

async def send_text_async(msg: str):
    client_config = ClientConfig()
    client = ClientFactory(client_config).create(agent1_card)

    message = Message(
        message_id=str(uuid.uuid4()),
        role="user",
        parts=[Part(root=TextPart(text=msg))]
    )

    last_event = None
    async for event in client.send_message(message):
        last_event = event

    if last_event and hasattr(last_event, "message") and last_event.message.parts:
        return last_event.message.parts[0].root.text
    return None

def send_text(msg: str):
    return asyncio.run(send_text_async(msg))

if __name__ == "__main__":
    question = "What is the capital of France?"
    response = send_text(question)
    print("Response:", response)
