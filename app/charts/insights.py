from __future__ import annotations

import pandas as pd
import streamlit as st
import altair as alt


def insights(df_view: pd.DataFrame, alt_base_color: str) -> None:
    if df_view.empty:
        st.info("No records match the current filters.")
        return

    # Row 1
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.caption("Outbreaks by year")
        ts = df_view.groupby("year").size().reset_index(name="Outbreaks").sort_values("year")
        st.altair_chart(
            alt.Chart(ts)
            .mark_line(point=True, color=alt_base_color)
            .encode(x="year:O", y="Outbreaks:Q", tooltip=["year:O", "Outbreaks:Q"])  # keep ordinal for gaps
            .properties(height=220),
            use_container_width=True,
        )

    with r1c2:
        st.caption("Top 10 diseases ")
        top_disease = (
            df_view.groupby("disease").size().reset_index(name="count").sort_values("count", ascending=False).head(10)
        )
        st.altair_chart(
            alt.Chart(top_disease)
            .mark_point(filled=True, size=90, color=alt_base_color)
            .encode(x="count:Q", y=alt.Y("disease:N", sort="-x"), tooltip=["disease:N", "count:Q"])  
            .properties(height=220),
            use_container_width=True,
        )

    # Row 2
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.caption("All diseases")
        all_disease = df_view.groupby("disease").size().reset_index(name="count")
        st.altair_chart(
            alt.Chart(all_disease)
            .mark_bar(color=alt_base_color)
            .encode(x=alt.X("disease:N", sort="-y"), y="count:Q", tooltip=["disease:N", "count:Q"])
            .properties(height=360),
            use_container_width=True,
        )

    with r2c2:
        st.caption("Top countries")
        if "iso3" in df_view.columns:
            by_country = (
                df_view.groupby(["country", "iso3"]).size().reset_index(name="Outbreaks").sort_values("Outbreaks", ascending=False).head(10)
            )
        else:
            by_country = (
                df_view.groupby("country").size().reset_index(name="Outbreaks").sort_values("Outbreaks", ascending=False).head(10)
            )
        st.altair_chart(
            alt.Chart(by_country)
            .mark_bar(color=alt_base_color)
            .encode(x="Outbreaks:Q", y=alt.Y("country:N", sort="-x"), tooltip=["country:N", "Outbreaks:Q"])
            .properties(height=360),
            use_container_width=True,
        )
