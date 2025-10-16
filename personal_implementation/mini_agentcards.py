# agent_cards.py
AGENT1_PORT = 8001
AGENT2_PORT = 8002
AGENT3_PORT = 8003

agent1_card = {
    "name": "Agent1",
    "url": f"http://localhost:{AGENT1_PORT}/a2a/v1"
}

agent2_card = {
    "name": "Agent2",
    "url": f"http://localhost:{AGENT2_PORT}/a2a/v1"
}

agent3_card = {
    "name": "Agent3",
    "url": f"http://localhost:{AGENT3_PORT}/a2a/v1"
}

ROUTING_MAP = {
    "search": agent2_card,
    "math": agent3_card
}
