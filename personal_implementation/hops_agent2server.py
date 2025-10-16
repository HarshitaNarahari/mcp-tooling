#hops_agent2server.py
from utils.server import run_agent_blocking
from agent_cards import agent2_card
from config import AGENT2_PORT, MODEL_NAME, OLLAMA_URL
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from utils.protocol_wrappers import extract_text
import ollama
import uuid
from a2a.types import Part, TextPart, Message, Role
from typing import cast

ollama_client = ollama.Client(host=OLLAMA_URL)

def query_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    response = ollama_client.generate(model=model, prompt=prompt)
    return response["response"].strip()

class SearchExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        query = extract_text(context.message) if context.message else ""
        print(f"[Agent2] Received: {query}")
        if not query.strip():
            return

        result = query_ollama(f"Answer this search question: {query}")
        print(f"[Agent2] Answer: {result}")

        parts = cast(list[Part], [TextPart(text=result)])
        msg = Message(message_id=str(uuid.uuid4()), role=Role.agent, parts=parts)

        await event_queue.enqueue_event(msg)
        print(f"[Agent2] Response enqueued successfully.")

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        return

if __name__ == "__main__":
    print(f"Agent2 (Search) running on port {AGENT2_PORT}")
    run_agent_blocking("Agent2", AGENT2_PORT, agent2_card, executor=SearchExecutor())
