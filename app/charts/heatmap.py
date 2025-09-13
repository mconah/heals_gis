from __future__ import annotations

import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
from scipy.interpolate import griddata


def generate_sample_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Generate sample coordinates for countries that don't have lat/lon data."""
    country_coords = {
        'Nigeria': {'lat': 9.0820, 'lon': 8.6753},
        'Ghana': {'lat': 7.9465, 'lon': -1.0232},
        'Kenya': {'lat': -0.0236, 'lon': 37.9062},
        'South Africa': {'lat': -30.5595, 'lon': 22.9375},
        'Ethiopia': {'lat': 9.1450, 'lon': 40.4897},
        'Uganda': {'lat': 1.3733, 'lon': 32.2903},
        'Tanzania': {'lat': -6.3690, 'lon': 34.8888},
        'Democratic Republic of the Congo': {'lat': -4.0383, 'lon': 21.7587},
        'Cameroon': {'lat': 7.3697, 'lon': 12.3547},
        'Mali': {'lat': 17.5707, 'lon': -3.9962},
        'Burkina Faso': {'lat': 12.2383, 'lon': -1.5616},
        'Niger': {'lat': 17.6078, 'lon': 8.0817},
        'Chad': {'lat': 15.4542, 'lon': 18.7322},
        'Sudan': {'lat': 12.8628, 'lon': 30.2176},
        'Angola': {'lat': -11.2027, 'lon': 17.8739},
        'Madagascar': {'lat': -18.7669, 'lon': 46.8691},
        'Mozambique': {'lat': -18.6657, 'lon': 35.5296},
        'Zambia': {'lat': -13.1339, 'lon': 27.8493},
        'Zimbabwe': {'lat': -19.0154, 'lon': 29.1549},
        'Botswana': {'lat': -22.3285, 'lon': 24.6849}
    }

    np.random.seed(42)
    result_data = []
    for _, row in df.iterrows():
        country = row['country']
        outbreaks = row.get('Outbreaks', 1)
        if country in country_coords:
            base_lat = country_coords[country]['lat']
            base_lon = country_coords[country]['lon']
            for i in range(min(outbreaks, 5)):
                lat = base_lat + np.random.normal(0, 1.5)
                lon = base_lon + np.random.normal(0, 1.5)
                intensity = outbreaks + np.random.normal(0, outbreaks * 0.2)
                result_data.append({
                    'country': country,
                    'lat': lat,
                    'lon': lon,
                    'intensity': max(intensity, 0.1)
                })
    return pd.DataFrame(result_data)


def create_heatmap(df_view: pd.DataFrame, color_scale: str, region_filter: str = "Global") -> None:
    """Create a density heatmap of outbreak occurrences."""
    if df_view.empty:
        st.info("No records match the current filters.")
        return
    geo_data = df_view.groupby(["country"], dropna=True).size().reset_index(name="Outbreaks")
    coord_data = generate_sample_coordinates(geo_data)
    if coord_data.empty:
        st.info("No coordinate data available for heatmap visualization.")
        return
    fig = go.Figure()
    fig.add_trace(go.Densitymapbox(
        lat=coord_data['lat'],
        lon=coord_data['lon'],
        z=coord_data['intensity'],
        radius=40,
        colorscale=color_scale,
        showscale=True,
        hovertemplate='<b>Density: %{z:.1f}</b><br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>',
        colorbar=dict(
            title=dict(text="Outbreak Intensity", side="right"),
            thickness=15,
            len=0.7
        )
    ))
    fig.add_trace(go.Scattermapbox(
        lat=coord_data['lat'],
        lon=coord_data['lon'],
        mode='markers',
        marker=dict(size=8, color='white', opacity=0.8, sizemode='diameter'),
        text=coord_data['country'],
        hovertemplate='<b>%{text}</b><br>Intensity: %{marker.color:.1f}<extra></extra>',
        showlegend=False
    ))
    if region_filter == "Nigeria":
        center_lat, center_lon = 9.0820, 8.6753
        zoom = 5.5
    elif region_filter == "Africa":
        center_lat, center_lon = 0, 20
        zoom = 2.5
    else:
        center_lat, center_lon = 20, 0
        zoom = 1.5
    fig.update_layout(
        mapbox=dict(style="carto-positron", center=dict(lat=center_lat, lon=center_lon), zoom=zoom),
        margin=dict(l=0, r=0, t=40, b=0), height=600,
        title=dict(text="Disease Outbreak Density Heatmap", x=0.5, font=dict(size=18, color="#2c3e50"))
    )
    st.plotly_chart(fig, use_container_width=True)
