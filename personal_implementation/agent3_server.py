# agent3_server.py
from utils.server import run_agent_blocking
from agent_cards import agent3_card
from config import AGENT3_PORT, MODEL_NAME, OLLAMA_URL
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

class MathExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        """Handle incoming math queries, compute via Ollama, and enqueue response."""
        query = extract_text(context.message) if context.message is not None else ""
        print(f"[Agent3] Received: {query}")
        if not query.strip():
            return

        # Solve math problem and return numeric answer only
        result = query_ollama(f"Solve this math problem and return only the numeric answer: {query}")
        print(f"[Agent3] Answer: {result}")

        # Wrap response in Message
        parts = cast(list[Part], [TextPart(text=result)])
        msg = Message(
            message_id=str(uuid.uuid4()),
            role=Role.agent,
            parts=parts
        )

        # Enqueue event properly
        await event_queue.enqueue_event(msg)
        print(f"[Agent3] Response enqueued successfully.")

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Optional: handle cancellation requests"""
        return

if __name__ == "__main__":
    print(f"Agent3 (Math) running on port {AGENT3_PORT}")
    run_agent_blocking("Agent3", AGENT3_PORT, agent3_card, executor=MathExecutor())
