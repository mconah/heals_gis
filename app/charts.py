from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt


def choropleth(df_view: pd.DataFrame, color_scale: str) -> None:
    if df_view.empty:
        st.info("No records match the current filters.")
        return
    geo = (
        df_view.groupby(["iso3", "Country"], dropna=True)
        .size()
        .reset_index(name="Outbreaks")
    )
    fig = px.choropleth(
        geo,
        locations="iso3",
        color="Outbreaks",
        hover_name="Country",
        color_continuous_scale=color_scale,
        projection="natural earth",
        title=None,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)


def insights(df_view: pd.DataFrame, alt_base_color: str) -> None:
    if df_view.empty:
        st.info("No records match the current filters.")
        return

    # Row 1
    r1c1, r1c2, r1c3 = st.columns([1.2, 1.6, 1.2])
    with r1c1:
        st.caption("Top 3 diseases")
        top3 = df_view["Disease"].value_counts().nlargest(3).reset_index()
        top3.columns = ["Disease", "Outbreaks"]
        st.altair_chart(
            alt.Chart(top3)
            .mark_bar(color=alt_base_color)
            .encode(x="Outbreaks:Q", y=alt.Y("Disease:N", sort="-x"), tooltip=["Disease:N", "Outbreaks:Q"])
            .properties(height=220),
            use_container_width=True,
        )

    with r1c2:
        st.caption("Outbreaks by year")
        ts = df_view.groupby("Year").size().reset_index(name="Outbreaks").sort_values("Year")
        st.altair_chart(
            alt.Chart(ts)
            .mark_line(point=True, color=alt_base_color)
            .encode(x="Year:O", y="Outbreaks:Q", tooltip=["Year:O", "Outbreaks:Q"])  # keep ordinal for gaps
            .properties(height=220),
            use_container_width=True,
        )

    with r1c3:
        st.caption("Top 20 diseases (dot plot)")
        top_disease = (
            df_view.groupby("Disease").size().reset_index(name="count").sort_values("count", ascending=False).head(20)
        )
        st.altair_chart(
            alt.Chart(top_disease)
            .mark_point(filled=True, size=90, color=alt_base_color)
            .encode(x="count:Q", y=alt.Y("Disease:N", sort="-x"), tooltip=["Disease:N", "count:Q"])
            .properties(height=220),
            use_container_width=True,
        )

    # Row 2
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.caption("All diseases (histogram)")
        all_disease = df_view.groupby("Disease").size().reset_index(name="count")
        st.altair_chart(
            alt.Chart(all_disease)
            .mark_bar(color=alt_base_color)
            .encode(x=alt.X("Disease:N", sort="-y"), y="count:Q", tooltip=["Disease:N", "count:Q"])
            .properties(height=360),
            use_container_width=True,
        )
    with r2c2:
        st.caption("Top countries")
        by_country = (
            df_view.groupby(["Country", "iso3"]).size().reset_index(name="Outbreaks").sort_values("Outbreaks", ascending=False).head(15)
        )
        st.altair_chart(
            alt.Chart(by_country)
            .mark_bar(color=alt_base_color)
            .encode(x="Outbreaks:Q", y=alt.Y("Country:N", sort="-x"), tooltip=["Country:N", "Outbreaks:Q"])  
            .properties(height=360),
            use_container_width=True,
        )

    # Row 3
    st.markdown("#### Outbreaks (filtered)")
    cols = [c for c in [
        "Year", "Country", "iso3", "Disease", "icd10n", "who_region", "unsd_region", "unsd_subregion", "DONs"
    ] if c in df_view.columns]
    table_df = df_view[cols].sort_values(["Year", "Country", "Disease"]).reset_index(drop=True)
    st.dataframe(table_df, use_container_width=True, hide_index=True)
