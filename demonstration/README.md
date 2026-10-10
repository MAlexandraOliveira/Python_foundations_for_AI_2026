# 🦅 FALC-ON AI — Deploy It on Streamlit Community Cloud

You need a **GitHub account** and a **Gemini API key** (see Class 9, *Step by step — get your free Gemini key*).

1. **Copy the course repository to your GitHub account:** open <https://github.com/MAlexandraOliveira/Python_foundations_for_AI_2026> and click **Fork** → **Create fork**.
2. Go to <https://share.streamlit.io> and click **Continue with GitHub** to sign in with your GitHub account.
3. Click **Create app** → **Deploy a public app from GitHub**.
4. Fill in:
   - **Repository:** `your-username/Python_foundations_for_AI_2026`
   - **Branch:** `main`
   - **Main file path:** `demonstration/falcon_ai_app.py`
5. Click **Advanced settings**:
   - **Python version:** choose **3.12**.
   - **Secrets:** paste this line, with your own key between the quotes:
     ```toml
     GEMINI_API_KEY = "your_key_here"
     ```
   - Click **Save**.
6. Click **Deploy**. After a minute or two, your app opens at its own web address, ending in `.streamlit.app`.

> ⚠️ Put your key **only** in the **Secrets** box — never in a file of the repository.
