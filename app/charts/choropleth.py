from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.express as px


def choropleth(df_view: pd.DataFrame, color_scale: str, region_filter: str = "Global") -> None:
    if df_view.empty:
        st.info("No records match the current filters.")
        return
    
    geo = (
        df_view.groupby(["iso3", "country"], dropna=True)
        .size()
        .reset_index(name="Outbreaks")
    )
    
    # Configure map scope based on region
    if region_filter == "Nigeria":
        # Focus on Nigeria
        fig = px.choropleth(
            geo,
            locations="iso3",
            color="Outbreaks",
            hover_name="country",
            color_continuous_scale=color_scale,
            projection="natural earth",
            title=None,
            scope="africa"  # Use Africa scope to better show Nigeria
        )
        # Further zoom into Nigeria region
        fig.update_geos(
            fitbounds="locations",
            visible=False
        )
    elif region_filter == "Africa":
        # Focus on Africa
        fig = px.choropleth(
            geo,
            locations="iso3",
            color="Outbreaks",
            hover_name="country",
            color_continuous_scale=color_scale,
            projection="natural earth",
            title=None,
            scope="africa"
        )
    else:
        # Global view
        fig = px.choropleth(
            geo,
            locations="iso3",
            color="Outbreaks",
            hover_name="country",
            color_continuous_scale=color_scale,
            projection="natural earth",
            title=None,
        )
    
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)
