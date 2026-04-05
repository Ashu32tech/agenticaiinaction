
import streamlit as st
from backend.graph import run_flow, execute_action

from dotenv import load_dotenv

load_dotenv(override=True)

st.title("🚀 DevOps Agentic AI")

query = st.text_input("Enter your issue")

if "state" not in st.session_state:
    st.session_state.state = None

if st.button("Run"):
    st.session_state.state = run_flow(query)

state = st.session_state.state

if state:
    st.subheader("🧠 Decision")
    st.json(state["decision"])

    st.subheader("📜 Logs")
    st.code(state["logs"])

    st.subheader("📚 RAG Context")
    st.write(state["context"])

    if st.button("✅ Approve"):
        result = execute_action(state)
        st.success(result)

    if st.button("❌ Reject"):
        st.warning("Action Rejected")
