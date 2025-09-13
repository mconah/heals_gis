from __future__ import annotations
import streamlit as st

def render_metrics(df):
    total_outbreaks = len(df)
    unique_countries = df['country'].nunique()
    unique_diseases = df['disease'].nunique()
    year_span = df['year'].max() - df['year'].min()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Total Outbreaks</div>
            <div class="metric-value">{total_outbreaks:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Countries Affected</div>
            <div class="metric-value">{unique_countries}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Disease Types</div>
            <div class="metric-value">{unique_diseases}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Year Span</div>
            <div class="metric-value">{year_span}+"</div>
        </div>
        """, unsafe_allow_html=True)
