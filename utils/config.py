import os
from openai import OpenAI

# Single source of truth for all model names in this course.
# Change a value here and every notebook picks it up automatically.
MODELS = {
    "chat": "gpt-5.4-mini",       # default — cheap, fast
    "frontier": "gpt-5.5",        # best quality; use sparingly
    "nano": "gpt-5.4-nano",       # ultra-cheap for high-volume demos
    "image": "gpt-image-1",       # image generation (DALL·E 3 retired May 2026)
    "stt": "gpt-4o-mini-transcribe",
    "tts": "gpt-4o-mini-tts",
}

# Approximate USD prices per 1 000 tokens (June 2026).
# Always verify current rates at https://openai.com/pricing before billing demos.
_COST_PER_1K = {
    "gpt-5.4-nano":  {"input": 0.00005,  "output": 0.00020},
    "gpt-5.4-mini":  {"input": 0.00015,  "output": 0.00060},
    "gpt-5.4":       {"input": 0.00100,  "output": 0.00400},
    "gpt-5.5":       {"input": 0.00300,  "output": 0.01200},
    "gpt-5.5-pro":   {"input": 0.00600,  "output": 0.02400},
}


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. "
            "Copy .env.example → .env and paste your key, then re-run the setup cell."
        )
    return OpenAI(api_key=api_key)


def estimate_cost(usage, model: str = MODELS["chat"]) -> float:
    """Return estimated USD cost for a ChatCompletion usage object."""
    rates = _COST_PER_1K.get(model, {"input": 0.0, "output": 0.0})
    return (
        (usage.prompt_tokens / 1000) * rates["input"]
        + (usage.completion_tokens / 1000) * rates["output"]
    )
