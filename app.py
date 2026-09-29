import streamlit as st
from src.rag_chain import load_chain, ask

st.set_page_config(page_title="Ask About Disha", page_icon="🌼", layout="centered")

st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container {max-width: 720px; padding-top: 2.5rem; padding-bottom: 6rem;}
html, body, [class*="css"] {font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;}
.hero {text-align:center; margin-bottom:1.5rem;}
.hero .logo {font-size:2.4rem; line-height:1;}
.hero h1 {font-size:1.9rem; font-weight:700; margin:.4rem 0 .3rem; letter-spacing:-.02em;}
.hero p {color:#5b564b; font-size:.95rem; margin:0;}
div.stButton > button {background:#F8F4EB; color:#1a1a1a; border:1px solid #d9d1bf; border-radius:14px;
  padding:.6rem .8rem; font-size:.85rem; width:100%; transition:all .15s;}
div.stButton > button:hover {background:#1a1a1a; color:#F8F4EB; border-color:#1a1a1a;}
[data-testid="stChatMessage"] {background:#F8F4EB; border:1px solid #e3dccb; border-radius:16px; padding:.8rem 1rem;}
[data-testid="stChatInput"] {border-radius:16px; background:#F8F4EB;}
[data-testid="stExpander"] {border:none; background:transparent;}
.small {font-size:.75rem; color:#7a7466;}
</style>
<div class="hero"><div class="logo">✿</div><h1>Ask About Disha</h1>
<p>Skills, projects, experience, education &amp; contact — ask anything.</p></div>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Getting things ready…")
def get_chain():
    return load_chain()


try:
    chain = get_chain()
except Exception as e:
    st.error(str(e))
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

SUGGESTIONS = ["Who is Disha?", "What are her top skills?", "Tell me about her projects",
               "Where did she study?", "What internships has she done?", "How can I contact her?"]

question = None
if not st.session_state.messages:
    for row in (SUGGESTIONS[:3], SUGGESTIONS[3:]):
        for col, s in zip(st.columns(3), row):
            if col.button(s, key=s):
                question = s

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="🙂" if m["role"] == "user" else "🌼"):
        st.markdown(m["content"])
        if m.get("sources"):
            st.markdown(f'<span class="small">Based on: {", ".join(m["sources"])}</span>', unsafe_allow_html=True)

question = st.chat_input("Ask me anything about Disha…") or question
if question:
    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🙂"):
        st.markdown(question)
    with st.chat_message("assistant", avatar="🌼"):
        with st.spinner("Thinking…"):
            try:
                r = ask(question, chain, history)
            except Exception as e:
                r = {"answer": f"Sorry, something went wrong ({type(e).__name__}). Please try again.", "sources": []}
        st.markdown(r["answer"])
    st.session_state.messages.append({"role": "assistant", "content": r["answer"], "sources": r["sources"]})
    st.rerun()

if st.session_state.messages:
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()