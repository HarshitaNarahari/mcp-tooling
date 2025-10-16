import asyncio
import uuid

from a2a.types import TextPart, Message
from a2a.client import ClientFactory, ClientConfig
from agent_cards import agent1_card

# sends text to agent1 asynchronously
async def send_text_async(msg: str):
    # create a client (default config)
    client_config = ClientConfig()
    client = ClientFactory(client_config).create()

    # message object with a unique id and the user text
    message = Message(
        message_id=str(uuid.uuid4()),
        role="user",
        parts=[TextPart(text=msg)]
    )

    last_event = None
    try:
        # send the message and listen for responses (events)
        async for event in client.send_message(message):
            last_event = event
            # print partial responses if they exist
            if hasattr(event, "message") and event.message.parts:
                print("partial:", "".join(
                    p.text for p in event.message.parts if isinstance(p, TextPart)
                ))
    except Exception as e:
        # catch and print any errors
        print("error sending message:", e)
        return None

    # if we got a final event with message parts, return the text
    if last_event and hasattr(last_event, "message") and last_event.message.parts:
        return "".join(
            p.text for p in last_event.message.parts if isinstance(p, TextPart)
        )
    return None

# this wraps the async function so it can be called normally
def send_text(msg: str):
    return asyncio.run(send_text_async(msg))

# run a simple test when the file is executed directly
if __name__ == "__main__":
    question = "what is the capital of france?"
    response = send_text(question)
    print("response:", response)
