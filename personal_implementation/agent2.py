# agent2.py

from utils.llm_client import query_ollama
from utils.protocol_wrappers import extract_text, send_text_async, listen_for_text
from config import AGENT2_PORT
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

# Formats query for search task
async def search_task(query: str) -> str:
    return query_ollama(f"Answer this search question: {query}")

# Main async loop for Agent2
async def main():
    self_client = ClientFactory(ClientConfig()).create(
        minimal_agent_card(f"http://localhost:{AGENT2_PORT}/a2a/v1")
    )
    print("Agent2 (Search) running...")

    while True:
        # Wait for new message
        task_msg = await listen_for_text(self_client, callback=lambda m: m)
        if not task_msg:
            await asyncio.sleep(0.2)
            continue

        # Extract query from message
        query = extract_text(task_msg) or ""
        print(f"[Agent2] Received: {query}")

        if not query.strip():
            continue

        # Send query to Ollama for answer
        result = await search_task(query)
        print(f"[Agent2] Answer: {result}")

        # Send result back using first argument only
        await send_text_async(task_msg, result)  # reply_port removed

# Start Agent2
if __name__ == "__main__":
    asyncio.run(main())
