import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        .main{
            padding-top:1rem;
        }

        .stChatMessage{
            border-radius:12px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )