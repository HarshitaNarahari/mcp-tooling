from utils.protocol_wrappers import extract_text
from config import AGENT3_PORT
from agent_cards import agent3_card
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from utils.server import run_agent_blocking

class MathExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        task_text = extract_text(context.message.parts)
        print(f"[Agent3] Received task: {task_text}")
        try:
            result = str(eval(task_text))
        except Exception:
            result = "Could not calculate"
        return {"response": result}
    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        pass
if __name__ == "__main__":
    print("Agent3 running on port", AGENT3_PORT)
    run_agent_blocking("Agent3", AGENT3_PORT, agent3_card, executor=MathExecutor())
