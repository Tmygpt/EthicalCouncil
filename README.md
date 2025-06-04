# Ethical Client

## Project Overview
This repository implements a small multi-agent framework designed to collaboratively answer ethics-related questions by retrieving and summarizing scientific and religious research.
---

## ⚙️ Setup & Install

1. **Clone & enter**  
   ```bash
   git clone https://Tmygpt/EthicalClient.git
   cd EthicalClient
   ```

2. **Create & activate virtualenv**  
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync --all-groups
   ```

3. **Configure credentials**  
   Create a `.env` in the project root containing:  
   ```bash
   touch .env
   echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
   echo "OPENAI_API_KEU=your_openai_api_key_here" > .env
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

---

## 🎬 Running the Demo

### 1. Start your child A2A agents

```bash
# InputAgent (extracts keywords)
uv run python3 -m agents.input_agent --host localhost --port 10002

# CollectorAgent (fetches papers)
uv run python3 -m agents.collector_agent --host localhost --port 10001
```

> Each agent serves a JSON-RPC endpoint at `/` and advertises metadata at `/.well-known/agent.json`.

### 2. Start the Host OrchestratorAgent

```bash
uv run python3 -m agents.host_agent.entry --host localhost --port 10000
```

### 3. Use the CLI

```bash
uv run python3 -m app.cmd.cmd
```
---

## 📖 Architecture Overview

1. **Front-End Client**  
   - Web/Mobile/CLI → Issues A2A JSON-RPC calls to the Host Agent.

2. **Host OrchestratorAgent**  
   - **A2A branch:** `list_agents()` & `delegate_task(...)`.  
   - **MCP branch:** Discovers MCP servers, loads & exposes each tool.

3. **Child A2A Agents**
   - InputAgent and CollectorAgent handle keyword extraction and paper lookup.

4. **MCP Servers**  
   - Serve tool definitions & executions over stdio.

---

## 💡 Why This Design?

- **Modularity**: Easily add/remove agents or tools.  
- **Scalability**: Central orchestrator routes high volume.  
- **Flexibility**: LLM picks between programmatic and agent skills.  
- **Simplicity**: Leverages JSON-RPC & stdio protocols.