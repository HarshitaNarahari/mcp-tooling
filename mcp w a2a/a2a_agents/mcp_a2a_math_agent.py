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
from mcp.server.fastmcp import FastMCP
import ast
import operator as op

# next next step: routing agent directly to wolfram alpha tool?


#first do this:
#instead of calling ollama, call mcp math tool
#parsing task into parts

# Initialize Ollama client
ollama_client = ollama.Client(host=OLLAMA_URL)

# Create the MCP server
mcp = FastMCP("math_tool")

# Operators we’ll allow (no unsafe stuff)
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

# evaluate math expressions using these cases
def evaluate_expression(expr: str):
    def eval_node(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](eval_node(node.operand))
        else:
            raise ValueError("That expression uses something we don’t support.")

    try:
        tree = ast.parse(expr, mode="eval").body
        return eval_node(tree)
    except Exception as e:
        raise ValueError(f"Couldn’t evaluate expression: {e}")

# quick math tool
@mcp.tool()
def calculate(expression: str) -> dict:
    try:
        result = evaluate_expression(expression)
        return {"input": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


def query_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    """Send prompt to Ollama model and return response string."""
    response = ollama_client.generate(model=model, prompt=prompt)
    return response["response"].strip()

class MathExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        """Handle incoming math queries, compute via MCP tool first, fallback to Ollama."""
        query = extract_text(context.message) if context.message is not None else ""
        print(f"[Agent3] Received: {query}")
        if not query.strip():
            return

        # Try to compute using local math MCP tool
        try:
            result = calculate(query)
            if "error" not in result:
                final_answer = str(result["result"])
                print(f"[Agent3] Local math tool answer: {final_answer}")
            else:
                raise ValueError(result["error"])
        except Exception:
            # Fallback to Ollama if math tool fails
            final_answer = query_ollama(f"Solve this math problem and return only the numeric answer: {query}")
            print(f"[Agent3] Ollama fallback answer: {final_answer}")

        # Wrap response in Message
        parts = cast(list[Part], [TextPart(text=final_answer)])
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
