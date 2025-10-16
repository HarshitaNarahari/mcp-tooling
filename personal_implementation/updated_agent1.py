# agent1ollama.py

import ollama
from utils.protocol_wrappers import extract_text, send_text_async
from config import AGENT1_PORT, OLLAMA_URL, MODEL_NAME
from agent_cards import agent1_card, ROUTING_MAP
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from utils.server import run_agent_blocking
from a2a.types import Message, TextPart, Part, Role
import uuid
from typing import cast
import asyncio

# Ollama client instance
ollama_client = ollama.Client(host=OLLAMA_URL)

def query_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    response = ollama_client.generate(model=model, prompt=prompt)
    text = response["response"].strip()
    clean_text = text.replace("**", "").replace("\\(", "").replace("\\)", "")
    return clean_text

# Keep track of past routing results
response_history = []


class TaskDelegater(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        # Extract text from incoming request
        incoming_text = extract_text(context.message) if context.message else ""
        if not incoming_text:
            print("[Agent1] No incoming message to route")
            return

        print(f"[Agent1] Received task: {incoming_text}")

        # Determine routing
        task_lower = incoming_text.lower()
        if any(w in task_lower for w in ["who", "what", "when", "where", "why", "find", "search"]):
            target_card = ROUTING_MAP["search"]
        elif any(w in task_lower for w in ["add", "multiply", "sum", "divide", "calculate", "+", "-", "*", "/", "solve"]):
            target_card = ROUTING_MAP["math"]
        elif any(w in task_lower for w in ["write", "generate", "story", "article", "blog", "content"]):
            # ➜ New routing for Content Generator (Agent4)
            target_card = ROUTING_MAP["content"]
        else:
            target_card = ROUTING_MAP["search"]

        # Port of the downstream agent
        target_port = int(target_card.url.split(":")[-1].split("/")[0])

        result_obj = await send_text_async(target_port, incoming_text)
        result = extract_text(result_obj) if result_obj else "No response received"


        # Track history
        response_history.append((target_card.name, result))
        print(f"[Agent1] Final reply from {target_card.name}: {result}")

        # Wrap result in Message and enqueue back
        parts = cast(list[Part], [TextPart(text=result)])
        msg = Message(
            message_id=str(uuid.uuid4()),
            role=Role.agent,
            parts=parts
        )
        await event_queue.enqueue_event(msg)
        print("[Agent1] Response sent back to caller successfully.")

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        print("[Agent1] Task was canceled")
        return


if __name__ == "__main__":
    print("Agent1 running on port", AGENT1_PORT)
    run_agent_blocking("Agent1", AGENT1_PORT, agent1_card, executor=TaskDelegater())
