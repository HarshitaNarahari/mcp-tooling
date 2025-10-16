# # test_agents.py
# import asyncio
# from utils.protocol_wrappers import send_text_async
# from config import AGENT1_PORT

# async def test_agent1():
#     tests = [
#         "Search: What is the capital of France?",
#         "Math: 12 * 8 + 5"
#     ]
#     for msg in tests:
#         print(f"\n[Test] Sending to Agent1: {msg}")
#         response = await send_text_async(AGENT1_PORT, msg)
#         print(f"[Test] Final response: {response}")

# if __name__ == "__main__":
#     asyncio.run(test_agent1())




# test_agents.py

import asyncio
from config import AGENT1_PORT
from utils.protocol_wrappers import send_text_async
from a2a.types import Message, TextPart, Part, Task

# Utility to extract text from a Message object
def get_text_from_message(msg: Message) -> str:
    text_parts = []
    for part in msg.parts:
        if isinstance(part.root, TextPart):
            text_parts.append(part.root.text)
    return "\n".join(text_parts)


async def test_agent1():
    test_cases = [
        "What is the birthstone of september?",
        "17000 / 5",
        "17 * 5",
        "When is Rihanna's birthday?",
        "Generate a blog post about puppy adoption",
        "Write an article on unethical uses of AI"
    ]

    for msg in test_cases:
        print(f"\n[Test] Sending to Agent1: {msg}")
        response = await send_text_async(AGENT1_PORT, msg)

        # Only extract text if we got a Message
        if isinstance(response, Message):
            final_text = get_text_from_message(response)
        elif isinstance(response, Task):
            # You could optionally handle Task objects here
            final_text = f"Task returned: {response}"
        else:
            final_text = "No response received"

        print(f"[Test] Final response: {final_text}")


if __name__ == "__main__":
    asyncio.run(test_agent1())


