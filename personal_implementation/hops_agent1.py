# agent1ollama.py
import uuid
from typing import cast

import ollama
from utils.protocol_wrappers import extract_text, send_text_async
from config import AGENT1_PORT, OLLAMA_URL, MODEL_NAME
from agent_cards import agent1_card, ROUTING_MAP
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from utils.server import run_agent_blocking
from a2a.types import Message, TextPart, Part, Role

# ---------------- Ollama Client ----------------
ollama_client = ollama.Client(host=OLLAMA_URL)

def query_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    response = ollama_client.generate(model=model, prompt=prompt)
    text = response["response"].strip()
    return text.replace("**", "").replace("\\(", "").replace("\\)", "")

response_history: list[tuple[str, str]] = []


# ---------------- Agent1 Executor ----------------
class TaskDelegater(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        incoming_text = extract_text(context.message) if context.message else ""
        if not incoming_text:
            print("[Agent1] No incoming message to route")
            return
        print(f"[Agent1] Received task: {incoming_text}")

        # --- Simple planner: detect multi-step queries ---
        if self._needs_multi_step(incoming_text):
            print("[Agent1] Detected multi-step task")
            final_answer = await self._handle_multi_step(incoming_text, context)
        else:
            # Single-step fallback (original behavior)
            final_answer = await self._single_step(incoming_text)

        # Track and return final answer
        response_history.append(("final", final_answer))
        parts = cast(list[Part], [TextPart(text=final_answer)])
        msg = Message(message_id=str(uuid.uuid4()), role=Role.agent, parts=parts)
        await event_queue.enqueue_event(msg)
        print(f"[Agent1] Final response sent: {final_answer}")

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        print("[Agent1] Task was canceled")

    # ---------------- Helpers ----------------
    def _needs_multi_step(self, text: str) -> bool:
        """
        Heuristic for demo: if text contains both a search-like word and
        a math-like word, assume it needs two hops.
        """
        t = text.lower()
        search_keywords = ["who", "what", "when", "where", "why", "find", "search", "population"]
        math_keywords   = ["add", "multiply", "sum", "divide", "calculate", "%", "+", "-", "*", "/", "solve"]
        return any(w in t for w in search_keywords) and any(w in t for w in math_keywords)

    async def _single_step(self, query: str) -> str:
        """Original single-hop routing."""
        qlower = query.lower()
        if any(w in qlower for w in ["who", "what", "when", "where", "why", "find", "search"]):
            target_card = ROUTING_MAP["search"]
        elif any(w in qlower for w in ["add", "multiply", "sum", "divide",
                                       "calculate", "+", "-", "*", "/", "solve", "%"]):
            target_card = ROUTING_MAP["math"]
        else:
            target_card = ROUTING_MAP["search"]

        target_port = int(target_card.url.split(":")[-1].split("/")[0])
        result_obj = await send_text_async(target_port, query)
        return extract_text(result_obj) if result_obj else "No response received"

    async def _handle_multi_step(self, query: str, context: RequestContext) -> str:
        """
        Example two-hop workflow:
          1. Ask Agent2 (search) for a fact.
          2. Use that fact in a new question to Agent3 (math).
        """
        context_id = getattr(context.call_context, "context_id", None)

        # --- First hop: search ---
        search_subquery = f"Find the key fact needed to answer: {query}"
        search_port = int(ROUTING_MAP["search"].url.split(":")[-1].split("/")[0])
        search_msg = await send_text_async(search_port, search_subquery,
                                           context_id=context_id)
        fact = extract_text(search_msg) if search_msg else ""
        print(f"[Agent1] Intermediate fact from Agent2: {fact}")

        # --- Second hop: math ---
        math_subquery = (
            f"Using the fact '{fact}', compute the final answer to the question: {query}"
        )
        math_port = int(ROUTING_MAP["math"].url.split(":")[-1].split("/")[0])
        math_msg = await send_text_async(math_port, math_subquery,
                                         context_id=context_id)
        final_answer = extract_text(math_msg) if math_msg else "No response received"
        print(f"[Agent1] Final result from Agent3: {final_answer}")
        return final_answer


# ---------------- Run Server ----------------
if __name__ == "__main__":
    print(f"Agent1 running on port {AGENT1_PORT}")
    run_agent_blocking("Agent1", AGENT1_PORT, agent1_card, executor=TaskDelegater())
