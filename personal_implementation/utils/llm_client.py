import ollama
from config import OLLAMA_URL, MODEL_NAME

# create one ollama client instance
ollama_client = ollama.Client(host=OLLAMA_URL)

def query_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    """Query Ollama and return sanitized response text."""
    response = ollama_client.generate(model=model, prompt=prompt)
    text = response["response"].strip()
    # strip basic markdown / latex formatting so other agents can parse it
    clean_text = text.replace("**", "").replace("\\(", "").replace("\\)", "")
    return clean_text
