# 📡 IdeaRadar

IdeaRadar is an AI-powered agentic pipeline built in a 48-hour War Room sprint. It takes a broad industry or topic as input, crawls the web for genuine user pain points, analyzes the data for the highest-value business opportunities, and automatically generates a comprehensive "Founder's Dossier" (Blueprint) in Markdown.

## 🏗 Architecture (The Pipeline)

IdeaRadar utilizes a sequential chain of 3 specialized Agents built with **LangGraph**:

1. **Agent A (The Scout):** Uses the `Tavily API` to crawl Reddit for "Pain Point" signals related to your topic.
2. **Agent B (The Analyst):** Powered by `Ollama` (`qwen3.5:cloud`), it filters the noise, extracts distinct business problems, and scores them based on sentiment and frequency to find the ultimate "Market Opportunity."
3. **Agent C (The Strategist):** Powered by `Ollama`, it takes the winning problem and authors a full "Founder's Dossier," detailing the Market Opportunity, MVP Features, Tech Stack, and a 4-week Roadmap.
4. **UI (The Dashboard):** A premium **Streamlit** frontend that streams the agent progress in real-time and provides a beautiful interface to view and download the blueprint.

## 🚀 Streamlit Cloud Deployment

1. **Push to GitHub**: Push your code to a public or private repository.
2. **Deploy**: Link your repo to Streamlit Cloud.
3. **CRITICAL: Set Secrets**: 
   Go to **Settings > Secrets** in the Streamlit Dashboard and paste the following:

   ```toml
   TAVILY_API_KEY = "your_tavily_key"
   OLLAMA_BASE_URL = "your_cloud_url"
   OLLAMA_API_KEY = "your_cloud_key"
   APP_PASSWORD = "your_password"
   ```

## 🛠️ Tech Stack
- **Agents**: LangGraph + LangChain
- **Intelligence**: Tavily AI (Search)
- **Engine**: Ollama (Nemotron-3-Nano)
- **UI**: Streamlit

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- A [Tavily](https://tavily.com/) API Key.
- [Ollama](https://ollama.com/) installed and running locally with the `qwen3.5:cloud` model available (or modify `src/graph.py` to use a model you have pulled, e.g., `llama3`).

### 2. Installation

Clone the repository and set up a virtual environment:

```bash
git clone <your-repo-url>
cd RidarAI
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configuration

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Open `.env` and add your Tavily API key:
```env
TAVILY_API_KEY=your_actual_api_key_here
OLLAMA_BASE_URL=http://localhost:11434
```

### 4. Running the Application

Launch the Streamlit dashboard:

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser. Enter a target market (e.g., "SaaS Billing") and watch the Radar scan!

## 🛡️ Edge Cases Handled
- **No API Key?** The Scout agent will gracefully fall back to mock data so you can still test the UI.
- **Ollama Offline/Auth Errors?** The LLM nodes will catch the 403/connection errors and return fallback error text rather than crashing the Streamlit app.
- **Empty Topics?** The UI prevents launch until a topic is provided.
