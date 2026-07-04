import streamlit as st


import streamlit as st


def render_sidebar(conversations):

    st.sidebar.title("InsightFlow AI")

    st.sidebar.divider()

    st.sidebar.header("Conversations")

    for conversation in conversations:

        if st.sidebar.button(
            conversation["title"],
            key=conversation["_id"],   # <-- unique key
            use_container_width=True,
        ):

            st.session_state.conversation_id = conversation["_id"]

def render_upload():

    return st.sidebar.file_uploader(
        "Upload Document",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
    )


def render_chat(messages):

    for message in messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])