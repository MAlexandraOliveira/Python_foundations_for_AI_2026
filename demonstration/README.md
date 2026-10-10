# 🦅 FALC-ON AI — Course Assistant

AI-powered chatbot for the **Python Foundations for AI** course  
Porto Executive Academy × FALC-ON AI

Built with: Python · Streamlit · Google Gemini 2.5 Flash (free tier)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your Gemini API key

Get a free key at <https://aistudio.google.com> → “Get API Key”

Either set it as an environment variable named `GEMINI_API_KEY`, or put it in `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_key_here"
```

### 3. Run

```bash
streamlit run falcon_ai_app.py
```

The app opens at <http://localhost:8501>

## Files

```
falcon_ai_app.py          # main app
requirements.txt          # dependencies
.streamlit/secrets.toml   # API key (never commit this)
```
