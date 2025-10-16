from utils.protocol_wrappers import extract_text
from config import AGENT2_PORT
from agent_cards import agent2_card
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from utils.server import run_agent_blocking

class SearchExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        task_text = extract_text(context.message.parts)
        print(f"[Agent2] Received task: {task_text}")
        # dummy search reply
        answer = f"Search result for '{task_text}'"
        return {"response": answer}
    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        pass
    
if __name__ == "__main__":
    print("Agent2 running on port", AGENT2_PORT)
    run_agent_blocking("Agent2", AGENT2_PORT, agent2_card, executor=SearchExecutor())
