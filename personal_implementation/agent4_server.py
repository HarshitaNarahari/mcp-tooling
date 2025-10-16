# hops_agent4_content.py
from utils.server import run_agent_blocking
from agent_cards import agent4_card
from config import AGENT4_PORT, MODEL_NAME, OLLAMA_URL
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from utils.protocol_wrappers import extract_text
import ollama
import uuid
from a2a.types import Part, TextPart, Message, Role
from typing import cast

# Initialize Ollama client
ollama_client = ollama.Client(host=OLLAMA_URL)

def query_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    """Send prompt to Ollama model and return response string."""
    response = ollama_client.generate(model=model, prompt=prompt)
    return response["response"].strip()

class ContentGeneratorExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        """Handle incoming messages, query Ollama, and send generated content back."""
        query = extract_text(context.message) if context.message is not None else ""
        print(f"[Agent4] Received: {query}")
        if not query.strip():
            return

        # Query Ollama with a content-generation prompt
        result = query_ollama(
            f"Write a concise but engaging 200-word article or blog post based on this topic or data:\n\n"
            f"{query}\n\n"
            f"Make it clear, factual, and easy to read."
        )
        print(f"[Agent4] Generated Content: {result}")

        # Wrap generated text in a Message
        parts = cast(list[Part], [TextPart(text=result)])
        msg = Message(
            message_id=str(uuid.uuid4()),
            role=Role.agent,
            parts=parts,
        )

        # Enqueue event properly
        await event_queue.enqueue_event(msg)
        print(f"[Agent4] Response enqueued successfully.")

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Optional: handle cancellation requests"""
        return

if __name__ == "__main__":
    print(f"Agent4 (Content Generator) running on port {AGENT4_PORT}")
    run_agent_blocking("Agent4", AGENT4_PORT, agent4_card, executor=ContentGeneratorExecutor())
