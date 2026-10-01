# 🤖 Project Workspace & Engineering Guidelines

## 🛠️ Core Technology Stack
- **Backend Framework:** Python 3.11+ using FastAPI
- **RAG & Orchestration Framework:** LlamaIndex
- **Database & Vector Store:** Supabase (PostgreSQL with `pgvector`)
- **Git Strategy:** Semantic Commits (Angular convention)

---

## 📂 Target Project Directory Structure
All generated code, scripts, and tests must align exactly with this architectural layout:

```text
├── app/
│   ├── api/                 # API routers and version control
│   │   ├── v1/
│   │   │   └── endpoints/   # Chat, ingest, and health check endpoints
│   │   └── router.py        # Main API v1 routing switch
│   ├── core/                # System configuration and singletons
│   │   └── config.py        # Pydantic environment validation settings
│   ├── services/            # Core business logic processing engine
│   │   └── rag/             # LlamaIndex execution environment
│   │       ├── chunking.py  # Ingestion pipelines & text split strategies
│   │       └── engine.py    # Query engine setups and vector index lookups
│   ├── models/              # Pydantic schemas and database type maps
│   └── main.py              # Application entrypoint initialization
├── tests/                   # Pytest testing environment
│   ├── conftest.py          # Global top-level fixtures (App configuration overrides)
│   ├── api/                 # Endpoint & routing isolation test directory
│   │   ├── conftest.py      # FastAPI TestClient and endpoint fixtures
│   │   └── test_chat.py     # Live chat router and streaming behavior assertions
│   └── rag/                 # LlamaIndex execution test directory
│       ├── conftest.py      # Mock embedding models & test index configurations
│       └── test_pipeline.py # Chunking logic and retrieval accuracy assertions
├── AGENTS.md                # Permanent AI system instruction rules
├── TODO.md                  # Adaptive sprint task-tracking ledger
└── pyproject.toml           # Poetry/Pipenv/Ruff configuration file
```

---

## 📐 Phase 1: AI Agent Planning & Discovery Protocol

### 1. Mode Boundaries & Restrictions
- When the user switches to Plan Mode, act strictly as a read-only Principal Software Architect.
- **No Execution:** Do not write code, do not modify application files, and do not attempt to run software test suites, compilers, or linters during this phase.

### 2. Guided Discovery Interrogation (Options-Based Requirements Gathering)
- When a user introduces a new feature or idea, always begin in **Discovery Mode**.
- **The Interrogation Rule:** Do not generate a checklist immediately. Instead, analyze the raw request against the current codebase structure and ask 2 to 3 highly targeted, technical questions to clarify requirements, data flow, or edge cases.
- **The Options-Driven Constraint:** For every question asked, you **MUST** provide 2 to 3 practical engineering options complete with brief, clear technical trade-offs (e.g., speed, token memory usage, database scalability) for the user to select from. Focus options tightly on the Python/FastAPI/LlamaIndex stack.
- **Pacing:** Ask your clarifying questions clearly and wait for the user's answers before asking more or moving forward.
- **Architect Brake:** If the user states your questions are too superficial, pause and deeply evaluate data mutations, edge cases, and architectural boundaries before asking 3 new, highly technical options-driven questions.

### 3. Append-Only File Persistence
- **Never Overwrite:** Treat the root `TODO.md` file as a permanent, append-only engineering ledger. Never clear, delete, or overwrite past checkboxes or headers.
- **Location:** Read the existing `TODO.md` file first to maintain structural context, then append all new tasks to the absolute bottom of the file.
- **Structure:** Group the new tasks under a new, distinct markdown header named `## [Feature Name] Sprint`.

### 4. Task Generation & Checklist Formatting
- **Format:** All newly appended tasks must be formatted using binary Markdown checkboxes (`- [ ]`).
- **Granularity:** Break tasks down into atomic, isolated implementation steps grouped strictly by our target layers: Supabase/Data, Backend/FastAPI, LlamaIndex/RAG Pipeline, and Pytest.
- **Targeting:** For every single task checkbox, explicitly state the target file path or directory to give the Build Agent a precise destination matching the Target Project Directory Structure.
- **Termination Gate:** Once the `TODO.md` file is appended, output a single message presenting the new task block to the user and stop execution. Wait for explicit human approval before switching phases.

---

## ⚙️ Phase 2: Setup & Environmental Guardrails

### 1. Verification & Quality Commands
- **Build / Run Command:** `uvicorn app.main:app --reload`
- **Testing Trigger:** `pytest`
- **Lint / Format Trigger:** `ruff check . && ruff format .`

### 2. Environment Variables & Secret Management
- All environmental configuration variables must be processed via Pydantic Settings inside `app/core/config.py`.
- **Never Hardcode Secrets:** The AI must always look for and use the following keys via the config module:
  - `SUPABASE_URL` & `SUPABASE_SERVICE_ROLE_KEY`
  - `OPENAI_API_KEY` (or chosen LLM provider key)
- If a required local variable is missing from the environment, the AI must alert the user immediately instead of creating a fake string placeholder.

### 3. Directory & Import Architectural Rules
- All API routing switches must live strictly inside `app/api/`.
- All LlamaIndex ingestion, chunking, and index logic must be isolated inside `app/services/rag/`.
- **Strict Absolute Imports:** Absolute imports are required across the entire codebase (e.g., `from app.core.config import settings`). Relative imports (e.g., `from ..core import`) are strictly forbidden.

---

## 🔨 Phase 3: Build & Execution Guardrails

### 0. Incremental Build Mode — No Test Generation or Execution
- **Current Phase:** The backend is being built incrementally. The user performs manual testing.
- **Do NOT generate test files.** Do not create new files under `tests/`. Do not add test functions to existing test files.
- **Do NOT run `pytest`.** Do not execute any test suite. The user will manually verify behavior.
- **Do NOT modify existing test files** unless the user explicitly asks.
- **Verification is manual.** After completing a task, run `ruff check . && ruff format .` to ensure code quality, then commit. The user will test the feature manually.
- **This constraint is lifted only when the user explicitly says** that automated testing should resume. Until then, all testing instructions below are preserved for future use but must NOT be followed.

### 1. Atomic Execution Loop
- Operate strictly under a **Single Checkbox Execution Rule** [^1]. Take exactly one task from `TODO.md`, implement it, verify it, and log it before touching another task [^1].
- **Definition of "Log It":** "Log it" means to complete the task and leave changes in the working directory for the user to review. It does not mean writing console prints or application logger statements.
- **Explicit Checkbox Completion:** Immediately after a task is manually verified by the user, you **MUST** modify the `TODO.md` file, physically change that task's checkbox from `- [ ]` to `- [x]`, and save the file [^1]. Do not look at or begin a new task until this status update is written to disk [^1].
- Immediately after writing code for a checkbox, run `ruff check . && ruff format .` to clean syntax and formatting [^1].

### 2. Git Commits — Only on Explicit Instruction
- **Do NOT run `git commit` or any git commands that modify the repository unless the user explicitly instructs you to do so.**
- After completing a task, run `ruff check . && ruff format .` to ensure code quality, then stop and wait for the user's review.
- When the user explicitly says to commit, you are authorized to run terminal git commands to commit the code.
- You must strictly use the **Semantic Commits (Angular)** format for all commits. Match the task to these exact types:
  - `feat: ...` for a new endpoint, database schema, or pipeline logic.
  - `fix: ...` for correcting an error, query failure, or edge case.
  - `test: ...` for adding or refactoring test suites.
  - `refactor: ...` for structural code cleaning without behavior change.
- **Commit Workflow (only when explicitly instructed):**
  1. User says: "commit" or equivalent explicit instruction.
  2. If the user specifies file path(s), stage only those files: `git add <file1> <file2> ...`
  3. If the user does not specify file path(s), stage all changed files: `git add .`
  4. Run: `git commit -m "<type>(<scope>): <description>"`
  5. Update `TODO.md` by changing the task checkbox to `- [x]`.

### 3. Error Recovery Guardrails
- If the user reports a bug after manual testing, you have 2 autonomous attempts to fix the syntax or logical bug [^1].
- If the bug is not resolved after 2 attempts, declare the blocker to the user in the terminal and stop [^1]. Never enter a loop that pollutes the codebase [^1].
