import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from frontend.client import (
    upload_document,
    chat,
    get_conversations,
    get_messages,
)

from frontend.ui import (
    render_sidebar,
    render_upload,
    render_chat,
)

from frontend.theme import apply_theme


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="InsightFlow AI",
    layout="wide",
)

apply_theme()


# ==========================================================
# Session State
# ==========================================================

defaults = {
    "conversation_id": None,
    "document_id": None,
    "document_name": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# Sidebar
# ==========================================================

conversations = get_conversations()

render_sidebar(conversations)

uploaded_file = render_upload()


# ==========================================================
# Upload Document
# ==========================================================

if (
    uploaded_file is not None
    and uploaded_file.name != st.session_state.document_name
):

    with st.spinner("Extracting knowledge and indexing document..."):

        response = upload_document(uploaded_file)

    st.session_state.document_id = response["document_id"]

    st.session_state.document_name = response["filename"]

    # New document → new conversation
    st.session_state.conversation_id = None

    st.sidebar.success("Document indexed successfully!")


# ==========================================================
# Active Document
# ==========================================================

if st.session_state.document_name is not None:

    st.sidebar.divider()

    st.sidebar.markdown("### Active Document")

    st.sidebar.info(
        st.session_state.document_name
    )


# ==========================================================
# Load Conversation
# ==========================================================

messages = []



if st.session_state.conversation_id is not None:

    history = get_messages(
        st.session_state.conversation_id
    )
    st.session_state.document_id = history[
    "conversation"
    ]["document_id"]
    
    st.sidebar.write(
    "Conversation:",
    st.session_state.conversation_id,
    )

    st.sidebar.write(
    "Document:",
    st.session_state.document_id,
)

    messages = history["messages"]


# ==========================================================
# Render Chat History
# ==========================================================

render_chat(messages)


# ==========================================================
# Chat Input
# ==========================================================

question = st.chat_input(
    "Ask anything about your document...",
    disabled=(
        st.session_state.document_id is None
    ),
)


# ==========================================================
# Ask Question
# ==========================================================

if question:

    with st.chat_message("user"):
        st.markdown(question)

    with st.spinner("Thinking..."):

        response = chat(

            document_id=st.session_state.document_id,

            question=question,

            conversation_id=st.session_state.conversation_id,
        )

    st.session_state.conversation_id = response[
        "conversation_id"
    ]

    st.rerun()