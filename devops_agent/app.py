import streamlit as st
from backend.graph import run_flow, execute_action
from dotenv import load_dotenv

load_dotenv(override=True)

st.title("🚀 DevOps Agentic AI")

query = st.text_input("Enter your issue")

if "state" not in st.session_state:
    st.session_state.state = None

if "error" not in st.session_state:
    st.session_state.error = None


# ✅ SAFE execution (NO threading)
if st.button("Run") and query:
    with st.spinner("⏳ Running agent..."):
        result = run_flow(query)

        if "error" in result:
            st.session_state.error = result["error"]
        else:
            st.session_state.state = result


# ❌ Error display
if st.session_state.error:
    st.error(st.session_state.error)


state = st.session_state.state

# ✅ Display result
if state and "decision" in state:

    st.subheader("🧠 Decision")
    st.json(state["decision"])

    st.subheader("📜 Logs")
    st.code(state.get("logs", ""))

    st.subheader("📚 RAG Context")
    st.write(state.get("context", ""))

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve"):
            state["decision"]["requires_approval"] = False
            result = execute_action(state)
            st.success(result)

    with col2:
        if st.button("❌ Reject"):
            st.warning("Action Rejected")