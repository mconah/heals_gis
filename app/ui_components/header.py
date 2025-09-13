from __future__ import annotations
import streamlit as st


def inject_header_css(color: str) -> None:
    st.markdown(
        f"""
        <style>
          h1, h2, h3, h4, h5, h6 {{
            color: {color} !important;
            font-weight: 800 !important;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )
