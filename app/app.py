import streamlit as st
import requests

API_URL = "http://localhost:8000/query"

st.set_page_config(page_title="Agentic RAG Chat", layout="centered")
st.title("💬 Agentic RAG – Customer Support")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input("Ask a customer support question..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(
        API_URL,
        json={"query": prompt}
    )
    answer = response.json()["answer"]

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
    with st.chat_message("assistant"):
        st.markdown(answer)
