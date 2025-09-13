import streamlit as st
import altair as alt
import pandas as pd

from app.data import load_data, filter_df
from app.ui import sidebar, inject_header_css
from app.charts import (
    choropleth as choropleth_chart,
    insights as insights_charts,
    heatmap_and_isoline_page
)


def init_app() -> None:
    """Initialize Streamlit config and theme."""
    st.set_page_config(
        page_title="GIS Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    alt.theme.enable("default")
    # Theme enabled in init_app
def load_data_with_refresh() -> pd.DataFrame:
    """Load data, handling manual refresh and showing toasts."""
    force_refresh = st.session_state.get('refresh_data', False)
    if force_refresh:
        st.session_state.refresh_data = False
        with st.spinner('Refreshing data from database...'):
            df = load_data(force_refresh=force_refresh)
        data_source = st.session_state.get('data_source', 'unknown')
        if data_source == 'database':
            st.toast("Data refreshed successfully from database!")
        elif data_source == 'csv':
            st.toast("Database unavailable, loaded from CSV backup")
        else:
            st.toast("Data refresh failed, using dummy data")
    else:
        df = load_data(force_refresh=force_refresh)
    return df


def apply_filters(
    df: pd.DataFrame,
    years_selected: list[int],
    selected_category: str,
    selected_diseases: list[str],
    region_filter: str
) -> pd.DataFrame:
    """Filter data by years, category, diseases, and region."""
    df_filtered = filter_df(df, years_selected, selected_category, selected_diseases)
    # Regional filter
    if region_filter == "Nigeria":
        if "iso3" in df_filtered.columns:
            df_filtered = df_filtered[df_filtered["iso3"] == "NGA"]
        else:
            df_filtered = df_filtered[df_filtered["country"].str.contains("Nigeria", case=False, na=False)]
    elif region_filter == "Africa" and "unsd_region" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["unsd_region"] == "Africa"]
    return df_filtered


def main() -> None:
    # Initialize app and load data
    init_app()
    df = load_data_with_refresh() if 'load_data_with_refresh' in globals() else load_data()
    # Sidebar selections
    (
        page,
        years_selected,
        color_theme,
        alt_base_color,
        region_filter,
        selected_category,
        selected_diseases
    ) = sidebar(df)
    # Display header
    years_label = (
        "All years"
        if len(years_selected) == len(sorted(df["year"].unique(), reverse=True))
        else ", ".join(map(str, years_selected))
    )
    region_label = f" — Region: {region_filter}" if region_filter != "Global" else ""
    st.subheader(f"{page} — Years: {years_label}{region_label}")
    # Filter data and render page
    df_view = apply_filters(df, years_selected, selected_category, selected_diseases, region_filter)
    if page == "Choropleth":
        choropleth_chart(df_view, color_theme, region_filter)
    elif page == "Heatmaps & Isolines":
        inject_header_css("#667eea")
        heatmap_and_isoline_page(df_view, color_theme, region_filter)
    else:
        insights_charts(df_view, alt_base_color)


if __name__ == "__main__":
    main()

