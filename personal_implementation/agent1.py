import uuid
import shutil
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks.task_updater import TaskUpdater
from a2a.utils.message import get_message_text
from utils.protocol_wrappers import extract_text, send_text, listen_for_text
from utils.server import run_agent_blocking
from config import AGENT1_PORT
from agent_cards import agent1_card, ROUTING_MAP
from memory import new_session


#reach ollama, 

# Reset session memory
session = new_session()
shutil.copy(session, "chat_memory/session_current.json")

# Keep shared response history
response_history = []  # [(agent_name, response)]


class TaskDelegater(AgentExecutor):
    """Agent1 routes tasks to Agent2 (search) or Agent3 (math)."""

    async def execute(self, ctx: RequestContext, event_queue: EventQueue) -> None:
        task_text = get_message_text(ctx.task.input.parts)

        print(f"\n[Agent1] Received task: {task_text}")

        # Decide routing
        keywords_search = ["who", "when", "where", "why", "what", "find", "search"]
        keywords_math = ["add", "multiply", "sum", "divide", "subtract", "calculate", "+", "-", "*", "/", "solve"]

        target_agent = None
        if any(word in task_text.lower() for word in keywords_search):
            target_agent = ROUTING_MAP["search"]
            print(f"[Agent1] Routing task → Agent2 (Search)")
        elif any(word in task_text.lower() for word in keywords_math):
            target_agent = ROUTING_MAP["math"]
            print(f"[Agent1] Routing task → Agent3 (Math)")

        # Send to agent2/3 if matched
        if target_agent:
            # Add memory context if available
            if response_history:
                history_str = "\n".join(
                    f"{i+1}. {agent}: {answer}"
                    for i, (agent, answer) in enumerate(response_history)
                )
                enriched_task = f"History:\n{history_str}\nQuery: {task_text}"
            else:
                enriched_task = task_text

            # Log the enriched task being sent
            print(f"[Agent1] Sending enriched task to {target_agent.name}: {enriched_task}")

            # Forward the request
            send_text(target_agent.port, enriched_task, reply_port=agent1_card.port)
            result_msg = listen_for_text(agent1_card.url)
            result = extract_text(result_msg)

            # Record history
            response_history.append((target_agent.name, result))
            print(f"[Agent1] Response from {target_agent.name}: {result}")

            # Return the response upstream
            await ctx.update(ctx.task.success(result))
        else:
            fail_msg = "Sorry, I don't know how to handle that."
            print(f"[Agent1] Could not route task: {fail_msg}")
            await ctx.update(ctx.task.fail(fail_msg))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Reject task if cancelled."""
        if context.task_id:
            updater = TaskUpdater(
                event_queue,
                task_id=context.task_id,
                context_id=context.context_id or str(uuid.uuid4()),
            )
            await updater.reject()


if __name__ == '__main__':
    print("Agent1 listening on http://localhost:8001")
    run_agent_blocking(
        name='Agent1',
        port=AGENT1_PORT,
        agent_card=agent1_card,
        executor=TaskDelegater(),
    )





