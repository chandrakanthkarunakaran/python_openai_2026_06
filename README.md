# Python Applications with OpenAI

Teaching materials for the **Government Certified Professional Course on Python Applications with OpenAI**, delivered by the **MSME Technology Development Center, Chennai**.

This repository holds Jupyter notebooks, shared utilities, sample data, and mini-apps used across six live-coding sessions. Notebooks are **skeletons** — the instructor fills in key cells during class while students follow along.

---

## Course schedule

| Session | Notebook | Date | Topics |
|---------|----------|------|--------|
| 1 | `notebooks/weekend1/01_foundations.ipynb` | Sat 20 Jun 2026 | Python essentials for AI apps, OpenAI ecosystem, API key setup, first Chat Completions call, tokens & cost |
| 2 | `notebooks/weekend1/02_chat_applications.ipynb` | Sun 21 Jun 2026 | Chat Completions deep dive, multi-turn chat, parameters, CLI chatbot, Streamlit/Gradio UI |
| 3 | `notebooks/weekend2/03_advanced_conversational.ipynb` | Sat 27 Jun 2026 | Prompt engineering, structured outputs, tool calling, streaming, retries, Responses API intro |
| 4 | `notebooks/weekend2/04_multimodal.ipynb` | Sun 28 Jun 2026 | Image generation, speech-to-text, text-to-speech, vision input |
| 5 | `notebooks/weekend3/05_integration_agents.ipynb` | Sat 04 Jul 2026 | Multimodal integration, Responses API built-in tools, capstone kickoff |
| 6 | `notebooks/weekend3/06_capstone.ipynb` | Sun 05 Jul 2026 | Integrated app, testing, cost & safety guardrails, demo |

**Format:** 3 weekends (Sat + Sun), 4 hours per day (9:30 am – 1:30 pm IST) — 24 contact hours total.

---

## Prerequisites

- **Python 3.10+** (3.12 recommended)
- A computer with internet access during sessions
- An [OpenAI Platform](https://platform.openai.com/) account with billing enabled
- Basic familiarity with Python helps; we reintroduce essentials in Session 1

No prior LLM or API experience is assumed.

---

## Quick start

### 1. Clone the repository

```bash
git clone <repo-url>
cd python_openai_2026_06
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

```bash
cp .env.example .env
```

Edit `.env` and set your key:

```env
OPENAI_API_KEY=sk-...
MOCK=0
```

> **Never commit `.env`.** It is listed in `.gitignore`. Treat your API key like a password.

Get a key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys). Ensure your account has a payment method and usage limits configured before the first live session.

### 5. Launch Jupyter

From the **project root** (the folder that contains `utils/`):

```bash
jupyter notebook
```

Open the session notebook for the day (e.g. `notebooks/weekend1/01_foundations.ipynb`) and **run the setup cell first**. You should see a smoke-test message confirming the client is ready.

---

## Offline / no-key mode (`MOCK=1`)

If you do not have an API key yet, or want to explore notebook structure without spending credits, set in `.env`:

```env
MOCK=1
```

Notebooks that support mock mode return canned responses instead of calling the OpenAI API. Switch back to `MOCK=0` when you are ready for live API calls.

---

## Repository layout

```
python_openai_2026_06/
├── README.md                 ← you are here
├── requirements.txt          ← Python dependencies
├── .env.example              ← template for OPENAI_API_KEY and MOCK
├── utils/
│   ├── config.py             ← model names, client factory, cost helpers
│   └── helpers.py            ← pretty-print, retry, mock responses
├── data/                     ← sample audio, images, and text for exercises
├── notebooks/
│   ├── weekend1/             ← Sessions 1–2
│   ├── weekend2/             ← Sessions 3–4
│   └── weekend3/             ← Sessions 5–6
├── apps/                     ← Streamlit / Gradio mini-apps built in class
└── solutions/                ← instructor-only (not in repo; gitignored)
```

### Shared configuration

All notebooks import model names from `utils/config.py` — **do not hardcode model strings in notebook cells**. Change defaults in one place:

| Key | Model | Typical use |
|-----|-------|-------------|
| `chat` | `gpt-5.4-mini` | Default demos — cheap and fast |
| `frontier` | `gpt-5.5` | Highest quality; use sparingly |
| `nano` | `gpt-5.4-nano` | Ultra-cheap high-volume demos |
| `image` | `gpt-image-1` | Image generation |
| `stt` | `gpt-4o-mini-transcribe` | Speech-to-text |
| `tts` | `gpt-4o-mini-tts` | Text-to-speech |

---

## How to work through a session

1. Pull the latest changes before each class.
2. Activate your virtual environment and start Jupyter from the project root.
3. Open the day's notebook and run the **setup cell** — fix any errors before continuing.
4. Follow along as the instructor live-codes sections marked with `# --- live-code below ---`.
5. Complete **Exercise** cells on your own; compare notes with classmates or the instructor.
6. Read **Common pitfalls** and **Recap** at the end of each notebook.

---

## Billing and cost control

- API usage is **pay-as-you-go**. Small classroom demos on `gpt-5.4-mini` typically cost fractions of a cent per request.
- Every notebook that calls the API should print `response.usage` when cost is discussed — watch prompt and completion token counts.
- Set a **monthly budget and hard limit** in your [OpenAI usage settings](https://platform.openai.com/settings/organization/limits) before the course.
- Approximate rates live in `utils/config.py`; verify current pricing at [openai.com/pricing](https://openai.com/pricing).

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `OPENAI_API_KEY not found` | Missing or unread `.env` | Copy `.env.example` → `.env`, add key, restart kernel |
| `AuthenticationError` | Invalid or revoked key | Generate a new key; check for extra spaces in `.env` |
| `ModuleNotFoundError: utils` | Jupyter started outside project root | `cd` to repo root before `jupyter notebook`, re-run setup cell |
| `RateLimitError` | Too many requests | Wait and retry; use `retry()` helper; lower demo frequency |
| `model_not_found` | Wrong model name | Use `MODELS[...]` from `utils/config.py`, not a bare string |

If the setup cell fails, read the printed message — notebooks are written to surface friendly errors instead of raw tracebacks.

---

## API notes (June 2026)

The course uses the **current OpenAI API**, not legacy product names from older marketing material:

- **Chat Completions API** — taught first (Sessions 1–3)
- **Responses API** — introduced for agentic patterns and built-in tools (Sessions 3+)
- **DALL·E** — retired from the API; we use **`gpt-image-1`** for image generation
- **Assistants API** — sunsetting; we use Responses API + Conversations API instead

See `CLAUDE.md` in this repo for the full modernization reference (instructor / maintainer use).

---

## License and support

Course materials are provided for enrolled participants. For setup help during sessions, ask the instructor. For account or billing issues, use [OpenAI Help Center](https://help.openai.com/).
