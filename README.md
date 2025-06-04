# Ethical Client

## Project
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

```bash
honcho start
uv run python3 -m app.cmd.cmd
```
---

## Acknowledgements

1. https://github.com/theailanguage/a2a_samples/
2. https://arxiv.org
3. https://openalex.org

Thank you to arXiv for use of its open access interoperability.

---