# agent3.py

from utils.llm_client import query_ollama
from utils.protocol_wrappers import extract_text, send_text_async, listen_for_text
from config import AGENT3_PORT
from a2a.client import ClientFactory, ClientConfig, minimal_agent_card
import asyncio
import ollama
from config import OLLAMA_URL, MODEL_NAME

# Ollama client instance
ollama_client = ollama.Client(host=OLLAMA_URL)

# Sends prompt to Ollama model and returns text response
def query_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    response = ollama_client.generate(model=model, prompt=prompt)
    return response["response"].strip()

# Formats query for math task
async def math_task(query: str) -> str:
    return query_ollama(f"Solve this math problem and give only the final answer: {query}")

# Main async loop for Agent3
async def main():
    self_client = ClientFactory(ClientConfig()).create(
        minimal_agent_card(f"http://localhost:{AGENT3_PORT}/a2a/v1")
    )
    print("Agent3 (Math) running...")

    while True:
        # Wait for new message
        task_msg = await listen_for_text(self_client, callback=lambda m: m)
        if not task_msg:
            await asyncio.sleep(0.2)
            continue

        # Extract query from message
        query = extract_text(task_msg) or ""
        print(f"[Agent3] Received: {query}")
        
        if not query.strip():
            continue

        # Send query to Ollama for answer
        result = await math_task(query)
        print(f"[Agent3] Answer: {result}")

        # Send result back (reply_port removed)
        await send_text_async(task_msg, result)

# Start Agent3
if __name__ == "__main__":
    asyncio.run(main())
