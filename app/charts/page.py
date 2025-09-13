from __future__ import annotations

import pandas as pd
import streamlit as st
from app.charts.heatmap import create_heatmap
from app.charts.isoline import create_isoline_chart


def heatmap_and_isoline_page(df_view: pd.DataFrame, color_scale: str, region_filter: str = "Global") -> None:
    """Create a beautiful page combining heatmaps and isoline charts with insights."""
    # Custom CSS for beautiful styling
    st.markdown("""
    <style>
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-title {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }
    .insight-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if df_view.empty:
        st.info("🔍 No records match the current filters. Try adjusting your selections.")
        return
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    total_outbreaks = len(df_view)
    unique_countries = df_view['country'].nunique()
    unique_diseases = df_view['disease'].nunique()
    year_span = df_view['year'].max() - df_view['year'].min()
    
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
    
    st.markdown("---")
    
    # Main visualizations: stacked full-width charts
    # Heatmap takes full width
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    create_heatmap(df_view, color_scale, region_filter)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Isoline takes full width
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    create_isoline_chart(df_view, color_scale, region_filter)
    st.markdown('</div>', unsafe_allow_html=True)
