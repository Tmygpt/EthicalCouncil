# The Council of Ethical Dilemmas

The Council of Ethical Dilemmas is a multi-agent framework where specialized agents — Scholars, Collectors, Summarizers, and the Orchestrator — collaborate to deliberate on complex ethical questions.

By consulting both scientific knowledge and religious wisdom, the Council retrieves, studies, and synthesizes insights from modern research and ancient thought to provide thoughtful responses to your moral inquiries.

## The Council's chambers include:

* **InputAgent (The Scholar):** Extracts ethical and scientific concepts from your query.

* **CollectorAgent (The Archivist):** Retrieves ancient scrolls from the great libraries of arXiv and OpenAlex.

* **ProcessorAgent (The Scribe):** Uploads the collected PDFs to a Pinecone vector store using Azure OpenAI embeddings.


* **ScienceSummaryAgent (The Science Sage):** Uses Retrieval-Augmented Generation with GPT‑4o to answer the user's question from the stored documents.


* **EthicsSummaryAgent (The Ethics Sage):** Uses the same approach to provide ethical perspectives based on the stored documents.


* **OrchestratorAgent (The Elder):** Oversees the Council, coordinating the deliberations, managing tools, and guiding the agents' collaboration via Gemini’s ADK runner.



---

## Summoning the Council

1. **Call the council**  
   ```bash
   git clone https://Tmygpt/EthicalClient.git
   cd EthicalClient
   ```

2. **Prepare the Council Chamber**  
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync --all-groups
   ```

3. **Present the Sacred Credentials provided to you by the holy one**  
   Create a `.env` in the project root and enter this in the terminal:  
   ```bash
   touch .env
   echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
   echo "OPENAI_API_TYPE=azure" >> .env
   echo "OPENAI_API_BASE=https://tv01.openai.azure.com/" >> .env
   echo "OPENAI_API_VERSION=2023-03-15-preview" >> .env
   echo "OPENAI_ENGINE=your_engine" >> .env
   echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
   echo "PINECONE_API_KEY=your_pinecone_key" >> .env
 echo "PINECONE_HOST=https://research-paper-summary-anadlyy.svc.aped-4627-b74a.pinecone.io" >> .env
  ```

The Pinecone index `research-paper-summary` expects 1024‑dimension vectors generated
with Azure OpenAI's `text-embedding-3-large` model.

---

## To convene the Council and begin ethical inquiry:
```bash
honcho start
streamlit run app/cli/streamlit_app.py
```
---

## Acknowledgements

1. https://github.com/theailanguage/a2a_samples/
2. https://arxiv.org
3. https://openalex.org

Thank you to arXiv for use of its open access interoperability.

---
