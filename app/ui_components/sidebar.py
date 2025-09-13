from __future__ import annotations

from typing import List, Tuple
import streamlit as st
from PIL import Image

from app.config import COLOR_THEME_OPTIONS, ALT_BASE_COLORS, Paths
from app.data import years_sorted, filter_df


def sidebar(df) -> Tuple[str, List[int], str, str, str, str, List[str]]:
    """Render the sidebar and return selections.

    Returns: (page, years_selected, color_theme, alt_base_color, region_filter, selected_category, selected_diseases)
    """
    with st.sidebar:
        # Logo display
        """
        try:
            img = Image.open(Paths.LOGO)
            st.image(img, caption="GIS Dashboard", use_container_width=True)
        except Exception:
            st.caption("Logo not found")
        """
        
        # Refresh data button
        data_source = st.session_state.get('data_source', 'unknown')
        if data_source in ['dummy', 'error']:
            refresh_clicked = st.button("🔄 Retry Connection", help="Retry loading data from database", type="primary")
        else:
            refresh_clicked = st.button("🔄 Refresh Data", help="Click to reload data from database")
        if refresh_clicked:
            st.session_state.refresh_data = True

        # Page selection
        page = st.radio("Select Page", ["All insights", "Choropleth", "Heatmaps & Isolines"], horizontal=False)

        # Region filter
        st.caption("Data Region Filter")
        region_options = ["Global", "Africa", "Nigeria"]
        region_filter = st.radio(
            "Select data region:", region_options, index=0,
            help="Choose which region to filter the data and visualizations"
        )

        # Year selection
        ys = years_sorted(df)
        year_choice = st.selectbox("Year", ["All years"] + [str(y) for y in ys])
        if year_choice != "All years":
            extra_years = st.multiselect("Add more years",
                                         [str(y) for y in ys if str(y) != year_choice])
            years_selected = sorted({int(year_choice)} | set(map(int, extra_years)), reverse=True)
        else:
            years_selected = ys

        # Color theme selection
        color_theme = st.selectbox("Color theme", COLOR_THEME_OPTIONS, index=1)
        alt_base_color = ALT_BASE_COLORS.get(color_theme, "#1f77b4")

        st.divider()
        
        # Data filters
        st.caption("Data Filters")
        categories = ["All"] + sorted([c for c in df["icd10n"].dropna().unique().tolist() if c])
        selected_category = st.selectbox("Category", categories)

        df_pool = filter_df(df, years_selected, selected_category)
        disease_options = df_pool["disease"].value_counts().sort_values(ascending=False).index.tolist()
        selected_diseases = st.multiselect("Diseases", disease_options, default=[])

    return page, years_selected, color_theme, alt_base_color, region_filter, selected_category, selected_diseases
