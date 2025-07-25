import streamlit as st
import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.llm_client import gemini_chat_model

st.set_page_config(page_title="User Registration via Gemini", page_icon="🤖")
st.title("🤖 Gemini-Driven Registration Chat")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Chat form ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", key="user_input", placeholder="Ask me something (e.g. 'Register Sachin with sachin@gmail.com')")
    submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        st.session_state.chat_history.append(("You", user_input))

        with st.spinner("Gemini is thinking..."):
            response = asyncio.run(gemini_chat_model(user_input))
            st.session_state.chat_history.append(("Gemini", response))

# --- Display chat history ---
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")

# --- Show registrations ---
if st.button("📋 Show All Registrations"):
    import pandas as pd
    try:
        df = pd.read_csv("registrations.csv")
        if not df.empty:
            st.subheader("📌 Registered Users")
            st.dataframe(df)
        else:
            st.info("No registrations found yet.")
    except FileNotFoundError:
        st.warning("No registration file found.")
