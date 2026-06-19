# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> You are the teaching-assistant / pair-programmer for an instructor-led course. Read this fully before generating, editing, or answering anything in this repo.

---

## What this project is

This repo holds all teaching material for a **Government Certified Professional Course on "Python Applications with OpenAI"** (MSME Technology Development Center, Chennai).

- **Format:** 3 weekends, online, Sat + Sun, 4 hours per day (9:30 am – 1:30 pm IST) → 6 sessions, ~24 contact hours.
- **Dates:** 20, 21, 27, 28 June and 04, 05 July 2026.
- **Deliverable per session:** one Jupyter notebook (`.ipynb`) the instructor live-codes from. Notebooks ship as **skeletons** — comment-driven cells and `TODO` stubs — so the instructor fills them in live while students follow along.
- **Audience:** working professionals + freshers. Python is (re)introduced from basics, but ramps quickly. Assume mixed skill; never assume prior LLM/API experience.
- **Instructor:** experienced data/AI engineer. Prefers production-aware patterns even in teaching code (env management, error handling, cost control). Don't dumb down architecture, but keep the *student-facing* surface simple.

You operate in two modes (see **Behavior** section below): **Build mode** (scaffolding the repo before the course) and **Teaching mode** (live assistance during sessions).

---

## Current OpenAI API reality (READ — the flyer is outdated)

The marketing flyer lists products by their 2023 names. Several no longer exist. **Always generate code against the current API below, not the flyer wording.** When a flyer topic is stale, teach the modern equivalent and add a one-line markdown note explaining the change.

| Flyer says | Current reality (June 2026) | What to teach / use |
|---|---|---|
| ChatGPT / GPT-4 | Frontier: **gpt-5.5**, **gpt-5.5-pro**. Workhorses: **gpt-5.4**, **gpt-5.4-mini**, **gpt-5.4-nano**. Reasoning: **o4-mini**. | Default demos on **gpt-5.4-mini** (cheap, fast). Show frontier with **gpt-5.5** sparingly. |
| OpenAI API | Two interfaces coexist: **Chat Completions API** (simple, ubiquitous, ideal for fundamentals) and the **Responses API** (modern, agentic loop with built-in tools). | Teach **Chat Completions first** (Sessions 1–3), then introduce **Responses API** (Sessions 3+). |
| DALL·E 2 / DALL·E 3 | **Removed from the API on 12 May 2026.** | Use **`gpt-image-1`** / **`gpt-image-1-mini`** (or `gpt-image-2`), or the `image_generation` tool in the Responses API. Mention DALL·E only as history. |
| Whisper / Speech | **`whisper-1`** still works. Newer managed STT: **`gpt-4o-transcribe`**, **`gpt-4o-mini-transcribe`**, **`gpt-4o-transcribe-diarize`**. TTS: **`gpt-4o-mini-tts`**. | Teach STT with **`gpt-4o-mini-transcribe`** (or `whisper-1` as the classic). Keep realtime as a demo/mention, not a build. |
| OpenAI Codex | Old code-completion model **retired** (`codex-mini-latest` deprecated Feb 2026). | Teach "automating coding tasks" as **code generation with current models** + a conceptual look at agentic coding tools. Do **not** call a `codex` model endpoint. |
| OpenAI Gym (RL) | **Not an OpenAI product.** It's **Gymnasium**, maintained by the Farama Foundation. RL has nothing to do with the OpenAI API. | Treat as a **short conceptual / optional aside** using `gymnasium`. Don't over-invest session time here. |
| Assistants API | **Sunsets 26 Aug 2026.** | Do **not** build on Assistants. Use **Responses API** (+ Conversations API for server-side state). |
| Fine-tuning | Self-serve fine-tuning is **winding down** (announced May 2026). | Don't anchor the course on fine-tuning. Cover prompt engineering, structured outputs, tools, and RAG instead. |

**Never hardcode a model string in multiple places** — read it from `utils/config.py` so a single edit re-points the whole repo.

---

## Session map

| Session | File | Date | Topics |
|---|---|---|---|
| 1 | `notebooks/weekend1/01_foundations.ipynb` | Sat 20 Jun | Python essentials for AI apps, OpenAI ecosystem tour, API key + billing, SDK install, first Chat Completions call, tokens, cost estimation |
| 2 | `notebooks/weekend1/02_chat_applications.ipynb` | Sun 21 Jun | Chat Completions deep dive, message roles, multi-turn state, key parameters, CLI chatbot, minimal Streamlit/Gradio UI |
| 3 | `notebooks/weekend2/03_advanced_conversational.ipynb` | Sat 27 Jun | Prompt engineering patterns, structured outputs, function/tool calling, streaming, retries, first look at Responses API |
| 4 | `notebooks/weekend2/04_multimodal.ipynb` | Sun 28 Jun | Image generation (`gpt-image-1`), STT (`gpt-4o-mini-transcribe`), TTS (`gpt-4o-mini-tts`), text tasks (summarize/classify/extract), vision input |
| 5 | `notebooks/weekend3/05_integration_agents.ipynb` | Sat 04 Jul | Combining modalities, Responses API built-in tools (web_search, file_search/RAG, code_interpreter, image_generation), RL/Gymnasium aside, capstone kickoff |
| 6 | `notebooks/weekend3/06_capstone.ipynb` | Sun 05 Jul | Finish integrated app, testing/debugging/optimizing, cost & safety guardrails (moderation, rate limits), presentation & demo |

---

## Repo structure

```
openai-course/
├─ CLAUDE.md
├─ README.md                  # student setup guide (keys, install, run)
├─ requirements.txt           # openai, python-dotenv, jupyter, streamlit, pillow, gymnasium, tiktoken
├─ .env.example               # OPENAI_API_KEY=, MOCK=0
├─ .gitignore                 # .env, __pycache__, .ipynb_checkpoints, solutions/
├─ utils/
│  ├─ config.py               # MODELS dict, client factory, cost helpers — single source of truth
│  └─ helpers.py              # pretty_print, token/cost estimate, mock responses, retry wrapper
├─ data/                      # sample audio/images/text for exercises
├─ notebooks/
│  ├─ weekend1/
│  ├─ weekend2/
│  └─ weekend3/
├─ apps/                      # streamlit/gradio mini-apps built in sessions 2 & 6
├─ solutions/                 # instructor-only filled notebooks (keep private)
└─ slides/
```

`utils/config.py` must define a `MODELS` dict and a `get_client()` factory:

```python
MODELS = {
    "chat": "gpt-5.4-mini",
    "frontier": "gpt-5.5",
    "image": "gpt-image-1",
    "stt": "gpt-4o-mini-transcribe",
    "tts": "gpt-4o-mini-tts",
}
```

---

## Notebook skeleton convention

Every session notebook follows this cell order. Setup cells must be **runnable as-is**; teaching cells are comment/`TODO` stubs the instructor fills live. Do **not** write full solutions into student notebooks (those go in `solutions/`).

1. **Title + objectives (markdown)** — `# Session N — <Title>`, learning objectives, agenda with rough timings.
2. **Setup cell (code, RUNNABLE)** — imports, `load_dotenv()`, client init via `utils/config.py`, `MODEL` constant, "client is alive" smoke test.
3. **Section blocks** (repeat per topic):
   - Markdown header with 2–4 sentence concept explanation.
   - Code cell with comments/`TODO`s and a `# --- live-code below ---` marker where the instructor types.
4. **Checkpoint / exercise cells** — markdown `> Exercise:` prompt + empty code cell with `# your turn:` stub. 2–4 per notebook.
5. **Common pitfalls (markdown)** — short list of errors students will hit (auth, wrong model name, rate limit, JSON parse).
6. **Recap (markdown)** — 3–5 bullet takeaways.
7. **Homework / capstone increment (markdown)**.

**Notebook style rules:**
- Each notebook is self-contained and runnable from a fresh kernel after the setup cell.
- Prefer many small cells over few large ones (teaching pace).
- Add `MOCK = os.getenv("MOCK", "0") == "1"` in setup so notebooks can run offline with canned responses.
- Every API-calling cell must fail with a friendly printed message on missing/invalid key, not a raw traceback.
- Default to the cheap model; add a comment showing how to swap to `gpt-5.5`.

---

## Coding conventions

- Use the official **`openai`** Python SDK; instantiate one client (`OpenAI()`). Do not use the deprecated `openai.ChatCompletion` global style.
- Show **both** interfaces where it teaches something: Chat Completions for fundamentals, Responses API for agentic/tools material. Don't silently mix them in one example.
- Always reference models via the `MODELS` config, never a bare string in a notebook cell.
- Wrap network calls with the retry helper from `utils/helpers.py`; surface clean error messages.
- Print/inspect `response.usage` whenever cost is the teaching point.
- Keep example prompts short, in English, and relatable to an Indian professional audience.

---

## Behavior

### Build mode (before the course)
- When asked to "scaffold session N," generate the notebook per the skeleton convention with comment-driven stubs — **not** full solutions. Put any reference solution in `solutions/` only if explicitly asked.
- When asked to "scaffold everything," generate all six notebooks, `utils/`, `requirements.txt`, `.env.example`, `.gitignore`, and `README.md`.
- After generating notebooks, verify: setup cells import from `utils/config.py`, model names match the table above, no hardcoded keys.

### Teaching mode (during live sessions)
- Be fast and concrete. When the instructor says "show an example of X," produce a small, runnable cell, not an essay.
- When debugging student errors, diagnose the actual cause first (auth? wrong model name? JSON parse? rate limit?) before rewriting code.
- Generate quick formative checks on request: a 3-question quiz, a fill-in-the-blank cell, or a "spot the bug" snippet.
- If a student asks something beyond scope, give a 1–2 line answer and note where it fits later in the course.
- Prefer `gpt-5.4-mini`/`-nano` for live demos; flag when a request would be expensive.

### Always
- Honor the flyer's **structure**, but the **content/API must be current** (see table above). Add a short markdown note when you modernize a flyer term.
- Don't invent model names or endpoints. If unsure whether a model/feature is current, say so and suggest verifying on the OpenAI docs.

---

## Common task prompts

- Scaffold one session: *"Scaffold Session 3 notebook per CLAUDE.md."*
- Scaffold the whole repo: *"Build the full repo skeleton (utils, all 6 notebooks, requirements, README, .env.example)."*
- Fill solutions: *"Create the solved version of Session 2 in solutions/ — leave the student notebook as a skeleton."*
- Live help: *"Student hit `AuthenticationError` on the setup cell — diagnose."* / *"Give me a 3-question quick check on tool calling."*
- Modernization check: *"Scan all notebooks for deprecated models/endpoints and list fixes."*
