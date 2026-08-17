# 🔎 Multi-Agent Deep Research System

An AI-powered tool built with Streamlit that automatically researches any topic for you using 4 AI agents working together in a step-by-step pipeline.

Powered by **LangChain**, **Mistral AI**, and **Tavily**.

---

## ⚡ What it Does

Instead of manually searching the web and reading dozens of pages, this system handles the process end-to-end:

1. **🔍 Search Agent:** Finds the most recent and reliable web sources for your topic using Tavily.
2. **📖 Reader Agent:** Picks the best source URL and scrapes full webpage content using BeautifulSoup.
3. **✍️ Writer Agent:** Synthesizes all information into a structured report (Intro, Key Findings, Conclusion, Sources).
4. **🧐 Critic Agent:** Reviews the report quality, gives a score out of 10, highlights strengths, and suggests improvements.

---

## 📁 Project Structure

```text
.
├── app.py           # Streamlit web user interface
├── agents.py        # Search, Reader, Writer, and Critic agent definitions
├── pipeline.py      # Core execution pipeline logic
├── tools.py         # Web search and scraping tools
├── requirements.txt # Project dependencies
├── Procfile         # Deployment command for cloud hosting
└── .env             # Environment variables (API keys)
```

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/ATHARVA9777/Multi-Agent-DeepResearch.git
cd Multi-Agent-DeepResearch
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API keys
Create a `.env` file in the root directory and add your keys:

```ini
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Run the application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

*(Optional)* Run directly in terminal without the web interface:
```bash
python pipeline.py
```

---

## ☁️ Deployment (Railway)

1. Push your code to your GitHub repository.
2. Connect your repo to **Railway** (New Project → Deploy from GitHub repo).
3. Add `MISTRAL_API_KEY` and `TAVILY_API_KEY` under the **Variables** tab.
4. Railway will automatically detect `requirements.txt` and `Procfile` to run the app.

---

## 🔑 Required API Keys

| Key | Description | Get it here |
| :--- | :--- | :--- |
| `MISTRAL_API_KEY` | Powers the writing, search, and critique agents | [Mistral Console](https://console.mistral.ai/) |
| `TAVILY_API_KEY` | Enables real-time web searching | [Tavily AI](https://tavily.com/) |
