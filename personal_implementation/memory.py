import json, os
from datetime import datetime

MEMORY_DIR = "chat_memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

def new_session():
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(MEMORY_DIR, f"session_{session_id}.json")
    with open(path, "w") as f:
        json.dump([], f)
    return path

def add_message(session_path, role, content):
    with open(session_path, "r") as f:
        history = json.load(f)
    history.append({"role": role, "content": content})
    with open(session_path, "w") as f:
        json.dump(history, f, indent=2)

def load_history(session_path, n=None):
    with open(session_path, "r") as f:
        history = json.load(f)
    if n:
        return history[-n:]
    return history



