"""CLI chatbot — run from the project root: python apps/chatbot_cli.py"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

_root = Path(__file__).parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from utils.config import MODELS, get_client, estimate_cost
from utils.helpers import retry, mock_chat_response

MOCK   = os.getenv("MOCK", "0") == "1"
MODEL  = MODELS["chat"]
SYSTEM = "You are a helpful assistant for Indian professionals."

# ── Main chatbot loop ────────────────────────────────────────────────────────
# GOAL: Interactive CLI chatbot with persistent conversation history
# STEPS:
#   1. client = get_client()  (skip if MOCK)
#   2. messages = [{'role': 'system', 'content': SYSTEM}]
#   3. Print a welcome banner (model name, "type 'exit' to quit")
#   4. total_cost = 0.0
#   5. while True:
#        user_input = input("You: ").strip()
#        if not user_input or user_input.lower() in ("exit", "quit", "bye"):
#            print("Goodbye!"); break
#        # TODO: messages.append({'role': 'user', 'content': user_input})
#        # TODO: if MOCK: response = mock_chat_response()
#        #        else:   response = retry(lambda: client.chat.completions.create(
#        #                                    model=MODEL, messages=messages))
#        # TODO: reply = response.choices[0].message.content
#        # TODO: messages.append({'role': 'assistant', 'content': reply})
#        # TODO: print(f"Assistant: {reply}")
#        # TODO: total_cost += estimate_cost(response.usage, MODEL)
#        # TODO: print(f"  [tokens: {response.usage.total_tokens} | session cost: ${total_cost:.5f}]")
# --- live-code below ---


if __name__ == "__main__":
    pass
