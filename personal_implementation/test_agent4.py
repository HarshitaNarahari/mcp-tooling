from utils.protocol_wrappers import send_text
from config import AGENT4_PORT
resp = send_text(AGENT4_PORT, "Explain the impact of AI on climate change research.")
print(resp)
