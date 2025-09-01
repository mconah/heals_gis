from __future__ import annotations

from typing import List, Tuple
import streamlit as st
from PIL import Image

from .config import COLOR_THEME_OPTIONS, ALT_BASE_COLORS, Paths
from .data import years_sorted


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


def sidebar(df) -> tuple[str, List[int], str, str, str]:
    """Render the sidebar and return selections.

    Returns: (page, years_selected, color_theme, alt_base_color, header_color)
    """
    with st.sidebar:
        try:
            img = Image.open(Paths.LOGO)
            st.image(img, caption="GIS Dashboard", use_container_width=True)
        except Exception:
            st.caption("Logo not found")

        page = st.radio("Select Page", ["All insights", "Choropleth"], horizontal=False)

        ys = years_sorted(df)
        year_choice = st.selectbox("Year", ["All years"] + [str(y) for y in ys])
        if year_choice != "All years":
            extra_years = st.multiselect(
                "Add more years",
                [str(y) for y in ys if str(y) != year_choice],
            )
            years_selected = sorted({int(year_choice)} | set(map(int, extra_years)), reverse=True)
        else:
            years_selected = ys

        color_theme = st.selectbox("Color theme", COLOR_THEME_OPTIONS, index=0)
        alt_base_color = ALT_BASE_COLORS.get(color_theme, "#1f77b4")

    return page, years_selected, color_theme, alt_base_color
