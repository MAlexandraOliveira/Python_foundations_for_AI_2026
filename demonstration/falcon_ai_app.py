# ─────────────────────────────────────────────────────────────────────────────
# FALC-ON AI — Course Assistant
# Streamlit + Gemini 3.8 Flash
#
# Run:  streamlit run falcon_ai_app.py
# Env:  GEMINI_API_KEY must be set in .streamlit/secrets.toml or as env var
# ─────────────────────────────────────────────────────────────────────────────

import os

import streamlit as st
from google import genai
from google.genai import types

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FALC-ON AI",
    page_icon="🦅",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500&display=swap');

/* Root variables */
:root {
    --navy:    #0D1B2A;
    --mid:     #1A2E42;
    --steel:   #2C4A6E;
    --accent:  #F4703A;
    --accent2: #E8A838;
    --text:    #E8ECF0;
    --muted:   #8CA0B5;
    --card:    #162232;
}

/* Global */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--navy);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: var(--navy);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Header */
.falc-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 28px 0 8px 0;
    border-bottom: 1px solid var(--steel);
    margin-bottom: 6px;
}
.falc-icon {
    font-size: 2.6rem;
    line-height: 1;
}
.falc-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.65rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text);
    margin: 0;
}
.falc-title span {
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.falc-sub {
    font-size: 0.78rem;
    color: var(--muted);
    margin: 2px 0 0 0;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* Pill badges */
.badge-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin: 14px 0 20px 0;
}
.badge {
    background: var(--card);
    border: 1px solid var(--steel);
    color: var(--muted);
    font-size: 0.72rem;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 20px;
    letter-spacing: 0.03em;
}
.badge.accent {
    border-color: var(--accent);
    color: var(--accent);
}

/* Chat container */
[data-testid="stChatMessage"] {
    background: var(--card) !important;
    border: 1px solid var(--steel) !important;
    border-radius: 12px !important;
    margin-bottom: 10px !important;
    padding: 14px 16px !important;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    background: var(--mid) !important;
    border-color: var(--steel) !important;
}

/* Chat input */
[data-testid="stChatInput"] textarea {
    background: var(--card) !important;
    border: 1px solid var(--steel) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(244,112,58,0.15) !important;
}

/* Suggested questions */
.suggest-label {
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-family: 'Space Grotesk', sans-serif;
    margin-bottom: 8px;
}
.stButton > button {
    background: var(--card) !important;
    border: 1px solid var(--steel) !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-size: 0.80rem !important;
    font-family: 'Inter', sans-serif !important;
    text-align: left !important;
    width: 100% !important;
    padding: 8px 12px !important;
    transition: border-color 0.15s, color 0.15s !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--text) !important;
}

/* Thinking spinner */
.thinking-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    margin: 0 2px;
    animation: pulse 1.2s infinite;
}
.thinking-dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes pulse {
    0%, 100% { opacity: 0.2; transform: scale(0.8); }
    50%       { opacity: 1;   transform: scale(1.1); }
}

/* Footer */
.falc-footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.70rem;
    padding: 20px 0 10px 0;
    border-top: 1px solid var(--steel);
    margin-top: 24px;
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)

# ── Course knowledge ───────────────────────────────────────────────────────────
COURSE_KNOWLEDGE = """
COURSE: Python Foundations for AI
INSTITUTION: Porto Executive Academy (PEA) + FALC-ON AI
INSTRUCTORS: Alexandra Oliveira and Catarina Santos, both AI Engineers
TOTAL CLASSES: 10, of 3 hours each
START DATE: 17 October 2026
SCHEDULE: every Saturday and Tuesday - Class 1 on Sat 17 Oct, 2 Tue 20 Oct, 3 Sat 24 Oct,
  4 Tue 27 Oct, 5 Sat 31 Oct, 6 Tue 3 Nov, 7 Sat 7 Nov, 8 Tue 10 Nov, 9 Sat 14 Nov, 10 Tue 17 Nov 2026

COURSE OBJECTIVES:
By the end of the course, participants will be able to:
- Understand Python's role as the main language of modern AI systems
- Write clean, modular, reusable Python code
- Load, clean and analyse data, and prepare it as context for AI models
- Build data and AI pipelines from functions and objects
- Visualise data, and the variability and errors of AI systems
- Store data in a database, and combine SQL with Python
- Call an AI model (Google Gemini) from their own code, through its API
- Build a final AI application: an "AI Support Desk"

TARGET AUDIENCE:
- Professionals already in the workforce, in any functional area
- Complete beginners: no programming experience required
- Analysts, managers and decision-makers, consultants, engineers, researchers, trainers and teachers
- Anyone who wants to work with AI and data teams, or automate work with Python

METHODOLOGY:
- AI-first: every Python concept is introduced with a clear purpose in an AI application
- The same thread through every class: FALC-ON AI, a course assistant that grows from a few
  if/elif rules (Class 1) into an assistant with a real AI model and a memory (Class 9)
- Each class: a short exposition (up to about 45 minutes, in a Google Colab notebook),
  a break, then hands-on exercises in four levels of difficulty
- A final project built one piece per class

CLASS FORMAT:
- 3 hours per class: exposition, a break, then exercises
- Everything runs in Google Colab, in the browser: nothing to install, only a Google account

PROGRAMME (10 classes):

Class 1 — Python as the Language of AI
  Google Colab; print() and comments; variables and data types; casting and input(); operators;
  f-strings; decisions (if/elif/else); loops (while, for, break, continue).
  Capstone: FALC-ON AI, a first AI pipeline with a rule-based stand-in model.
  (The assistant you are talking to now is the Gemini-powered version of that chatbot, built with
   Streamlit — students see it in a live demo in Class 10.)

Class 2 — Data Structures for AI Systems
  Lists, sets and dictionaries; built-in functions and methods; JSON.
  Capstone: a conversation stored as a list of messages, the shape real AI models use.

Class 3 — Data Analysis with pandas
  Loading a CSV file; selecting and filtering; data quality (missing values, duplicates, messy text);
  removing personal data; new columns; summarising with groupby; saving to CSV and JSON.
  Capstone: preparing customer-support tickets as input for an AI assistant.

Class 4 — Functions as AI Pipelines
  Defining functions; parameters and return values; default arguments; docstrings.
  Capstone: FALC-ON AI rebuilt as a pipeline of small functions.

Class 5 — Comprehensions and Functional Thinking
  List, dictionary and set comprehensions; sorting with a key and lambda; map, filter, zip, any, all.
  Capstone: preparing a batch of questions for an AI model, and reusing its answers.

Class 6 — Data Visualisation for AI Insights
  matplotlib and seaborn: line, bar, histogram, scatter and box plots; a dashboard; saving charts.
  Capstone: an AI assistant dashboard, including how consistent a model's answers are.

Class 7 — Databases
  SQLite: creating tables, adding, reading, changing and deleting rows with SQL; pandas and SQL together.
  Capstone: FALC-ON AI gets a long-term memory of its conversations and ratings.

Class 8 — Object-Oriented Python for AI Systems
  Classes as templates; objects, attributes and methods; class variables; encapsulation; inheritance.
  Capstone: FALC-ON AI as two cooperating objects, an assistant and its memory.

Class 9 — AI Libraries and APIs
  The standard library; installing libraries and reproducibility; writing and importing your own
  module; web APIs and real-time data; LLMs and their providers; calling Google Gemini, with the
  API key kept secret.
  Capstone: FALC-ON AI gets a real AI model (Gemini), grounded in the course facts.

Class 10 — Final Project: the AI Support Desk
  Students hand in an application that loads and cleans customer-support tickets, stores them in
  SQLite, uses Gemini to classify each ticket and draft a reply, measures how good the AI is
  (accuracy, consistency, human ratings), and shows the results in charts.
  It is delivered as Google Colab notebooks written as a report. There is no oral presentation.
  Also, from slides and a live demo: Git and GitHub, and Streamlit — this app is that demo.

ASSESSMENT:
Two certificates:
1. Certificate of Attendance: for at least 75% attendance
2. Certificate with Grade: the final project, graded on data handling (15%), structure and
   logic (15%), object-oriented design (15%), database (15%), modules (10%), visualisation and
   analysis (15%), AI integration (10%), and report and communication (5%);
   plus a bonus of +1 point for the optional stretch goals
PROJECT DEADLINE: submit the final project on Moodle by Saturday, 21 November 2026

TOOLS USED IN THE COURSE:
- Google Colab (all classes)
- pandas (Class 3 onwards)
- matplotlib and seaborn (Class 6)
- SQLite (Class 7)
- Google Gemini API (Class 9 and the final project)
- Git/GitHub and Streamlit: introduced in Class 10 with a live demo
- All you need to start: a Google account"""

SYSTEM_PROMPT = f"""You are FALC-ON AI, the official AI assistant for the course "Python Foundations for AI",
offered by Porto Executive Academy (PEA) in partnership with FALC-ON AI, and taught by Alexandra Oliveira
and Catarina Santos.

Your role is to answer questions about this course and about Python/AI in general, in a way that is:
- Friendly, encouraging and accessible to beginners
- Concise — keep answers to 2-4 short paragraphs maximum
- Honest — if you don't know something specific about the course, say so clearly
- Always in the same language the user writes in (Portuguese or English)

Here is the complete course information you should use to answer questions:

{COURSE_KNOWLEDGE}

Important: if someone asks what you are or how you were built, you can say you are an AI assistant
powered by Google Gemini, built with Python and Streamlit. In Class 9, students call Gemini from their own
Python code, as this app does, and in Class 10 they see this app in a live demo.
"""

# ── Gemini client (cached) ────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    # Use the environment variable if it is set; otherwise read .streamlit/secrets.toml.
    # (Reading st.secrets with no secrets file shows a warning box, so only read it when needed.)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            api_key = None  # no secrets.toml either
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found. Add it to .streamlit/secrets.toml or set it as an env var.")
        st.stop()
    return genai.Client(api_key=api_key)

def get_chat():
    """Create or retrieve the chat session from Streamlit session state."""
    if "chat" not in st.session_state:
        client = get_client()
        st.session_state.chat = client.chats.create(
            model="gemini-3.8-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.35,
                max_output_tokens=600,
            )
        )
    return st.session_state.chat


def answer_prompt(prompt):
    """Show the user's message, get the assistant's reply, and store both."""
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🦅"):
        with st.spinner(""):
            try:
                answer = get_chat().send_message(prompt).text
            except Exception as e:
                answer = f"I ran into a problem answering that. Please try again. *(Error: {e})*"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="falc-header">
    <div class="falc-icon">🦅</div>
    <div>
        <p class="falc-title">FALC-ON <span>AI</span></p>
        <p class="falc-sub">Python Foundations for AI · Porto Executive Academy</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="badge-row">
    <span class="badge accent">Powered by Gemini 3.8 Flash</span>
    <span class="badge">Built with Python + Streamlit</span>
    <span class="badge">Free tier</span>
</div>
""", unsafe_allow_html=True)

# ── Suggested questions (only when no messages yet) ───────────────────────────
SUGGESTIONS = [
    "What will I be able to build by the end of this course?",
    "Do I need programming experience to join?",
    "How is each class structured?",
    "What tools will we use?",
    "What is the Class 10 final project?",
    "How is the course assessed?",
]

if not st.session_state.messages:
    st.markdown('<p class="suggest-label">Try asking</p>', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, suggestion in enumerate(SUGGESTIONS):
        with cols[i % 2]:
            if st.button(suggestion, key=f"sug_{i}"):
                st.session_state.pending_question = suggestion
                st.rerun()

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🦅" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# ── Handle pending question from suggestion buttons ───────────────────────────
if st.session_state.pending_question:
    prompt = st.session_state.pending_question
    st.session_state.pending_question = None
    answer_prompt(prompt)
    st.rerun()

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask me anything about the course..."):
    answer_prompt(prompt)

# ── Footer ────────────────────────────────────────────────────────────────────
if st.session_state.messages:
    st.markdown(
        '<div class="falc-footer">FALC-ON AI · Porto Executive Academy · '
        'Built with Python & Streamlit · Gemini 3.8 Flash</div>',
        unsafe_allow_html=True
    )
