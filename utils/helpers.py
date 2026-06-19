import time
from typing import Any, Callable

# Canned text returned when MOCK=1
_MOCK_TEXT = "[MOCK] This is a simulated response. Set MOCK=0 in .env to call the real API."


# ── Pretty-printing ────────────────────────────────────────────────────────

def pretty_print(response) -> None:
    """Print reply text plus token counts from a ChatCompletion response."""
    print("─" * 60)
    print(response.choices[0].message.content)
    print("─" * 60)
    u = response.usage
    print(f"  Tokens  prompt={u.prompt_tokens}  completion={u.completion_tokens}  total={u.total_tokens}")


# ── Retry helper ───────────────────────────────────────────────────────────

def retry(fn: Callable, retries: int = 3, delay: float = 2.0) -> Any:
    """Call fn(); on exception retry up to `retries` times with `delay` seconds between."""
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as exc:
            if attempt == retries:
                raise
            print(f"Attempt {attempt}/{retries} failed: {exc}  — retrying in {delay}s…")
            time.sleep(delay)


# ── Mock response ──────────────────────────────────────────────────────────

def mock_chat_response(content: str = _MOCK_TEXT):
    """Return a duck-typed fake ChatCompletion response for offline / MOCK=1 demos."""

    class _Usage:
        prompt_tokens = 12
        completion_tokens = 24
        total_tokens = 36

    class _Message:
        role = "assistant"
        def __init__(self, text):
            self.content = text

    class _Choice:
        finish_reason = "stop"
        def __init__(self, text):
            self.message = _Message(text)

    class _Response:
        model = "mock"
        def __init__(self, text):
            self.choices = [_Choice(text)]
            self.usage = _Usage()

    return _Response(content)


# ── Token / cost summary ───────────────────────────────────────────────────

def token_cost_summary(usage, model: str, cost_per_1k: dict) -> str:
    """Return a one-line cost breakdown string."""
    rates = cost_per_1k.get(model, {"input": 0.0, "output": 0.0})
    cost = (
        (usage.prompt_tokens / 1000) * rates["input"]
        + (usage.completion_tokens / 1000) * rates["output"]
    )
    return (
        f"prompt={usage.prompt_tokens} tok | "
        f"completion={usage.completion_tokens} tok | "
        f"total={usage.total_tokens} tok | "
        f"est. cost=${cost:.6f}"
    )
