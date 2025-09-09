import streamlit as st
import altair as alt

from app.data import load_data, filter_df
from app.ui import sidebar, inject_header_css
from app.charts import choropleth as choropleth_chart, insights as insights_charts


st.set_page_config(
    page_title="GIS Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

alt.theme.enable("default")


def main() -> None:
    df = load_data()

    page, years_selected, color_theme, alt_base_color = sidebar(df)

    # Right-side filter rail
    main_col, filter_col = st.columns([5, 2], gap="large")
    with filter_col:
        st.caption("Include non communicable diseases")
        _ = st.toggle("", value=True)

        categories = ["All"] + sorted([c for c in df["icd10n"].dropna().unique().tolist() if c])
        selected_category = st.selectbox("Category", categories)

        df_pool = filter_df(df, years_selected, selected_category)
        disease_options = (
            df_pool["disease"].value_counts().sort_values(ascending=False).index.tolist()
        )
        selected_diseases = st.multiselect("diseases", disease_options, default=[])

    with main_col:
        years_label = (
            "All years" if len(years_selected) == len(sorted(df["year"].unique(), reverse=True)) else ", ".join(map(str, years_selected))
        )
        st.subheader(f"{page} — Years: {years_label}")

        df_view = filter_df(df, years_selected, selected_category, selected_diseases)

        if page == "Choropleth":
            choropleth_chart(df_view, color_theme)
        else:
            insights_charts(df_view, alt_base_color)


if __name__ == "__main__":
    main()

