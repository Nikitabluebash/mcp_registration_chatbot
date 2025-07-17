import streamlit as st
import httpx

API_BASE = "http://localhost:8000"  # MCP backend running

st.title("📋 User Registration Chatbot")

if "state" not in st.session_state:
    st.session_state.state = "ASK_NAME"
    st.session_state.user_data = {}

def ask_question():
    if st.session_state.state == "ASK_NAME":
        st.text_input("What's your name?", key="name_input", on_change=submit_name)
    elif st.session_state.state == "ASK_EMAIL":
        st.text_input("What's your email?", key="email_input", on_change=submit_email)
    elif st.session_state.state == "ASK_DOB":
        st.date_input("What's your date of birth?", key="dob_input", on_change=submit_dob)
    elif st.session_state.state == "REGISTERED":
        st.success("✅ Registered successfully!")
        st.session_state.state = "ASK_NAME"
        st.session_state.user_data = {}

def submit_name():
    st.session_state.user_data["name"] = st.session_state.name_input
    st.session_state.state = "ASK_EMAIL"

def submit_email():
    st.session_state.user_data["email"] = st.session_state.email_input
    st.session_state.state = "ASK_DOB"

def submit_dob():
    st.session_state.user_data["dob"] = str(st.session_state.dob_input)

    try:
        with httpx.Client() as client:
            response = client.post(f"{API_BASE}/register", json=st.session_state.user_data)
            if response.json().get("status") == "success":
                st.session_state.state = "REGISTERED"
                st.session_state.user_data = {}
                return  # Exit early to let ask_question show success
            else:
                st.error("❌ Failed to register user.")
                return
    except Exception as e:
        st.error(f"❌ Network error: {e}")
        return

    # Only reset if success
    st.session_state.state = "ASK_NAME"
    st.session_state.user_data = {}


# Handle "show all registrations"
if st.button("📖 Show All Registrations"):
    with httpx.Client() as client:
        response = client.get(f"{API_BASE}/registrations")
        if response.status_code == 200:
            data = response.json()
            st.table(data)
        else:
            st.error("Failed to fetch registrations.")

# Run chatbot logic
ask_question()
