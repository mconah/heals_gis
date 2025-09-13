from __future__ import annotations

import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.interpolate import griddata
from .heatmap import generate_sample_coordinates


def create_isoline_chart(df_view: pd.DataFrame, color_scale: str, region_filter: str = "Global") -> None:
    """Create isoline (contour) charts showing outbreak patterns."""
    if df_view.empty:
        st.info("No records match the current filters.")
        return

    geo_data = df_view.groupby(["country"], dropna=True).size().reset_index(name="Outbreaks")
    # Generate coordinates and intensity for each country
    coord_data = generate_sample_coordinates(geo_data)
    if coord_data.empty:
        st.info("No coordinate data available for isoline visualization.")
        return

    # Create grid for interpolation
    if region_filter == "Nigeria":
        lat_range, lon_range = (6, 14), (3, 15)
    elif region_filter == "Africa":
        lat_range, lon_range = (-35, 37), (-18, 52)
    else:
        lat_range, lon_range = (-60, 80), (-180, 180)
    grid_lat = np.linspace(lat_range[0], lat_range[1], 50)
    grid_lon = np.linspace(lon_range[0], lon_range[1], 50)
    grid_lat_mesh, grid_lon_mesh = np.meshgrid(grid_lat, grid_lon)

    points = np.column_stack((coord_data['lat'], coord_data['lon']))
    values = coord_data['intensity']
    try:
        grid_intensity = griddata(points, values, (grid_lat_mesh, grid_lon_mesh), method='cubic', fill_value=0)
    except:
        grid_intensity = griddata(points, values, (grid_lat_mesh, grid_lon_mesh), method='linear', fill_value=0)

    fig = make_subplots(rows=1, cols=2, subplot_titles=('Contour Map', 'Surface Plot'),
                        specs=[[{'type': 'xy'}, {'type': 'scene'}]], horizontal_spacing=0.05)
    fig.add_trace(go.Contour(x=grid_lon_mesh[0], y=grid_lat_mesh[:, 0], z=grid_intensity,
                              colorscale=color_scale, showscale=True, line_width=2,
                              colorbar=dict(title=dict(text="Outbreak Intensity", side="right"),
                                            thickness=15, len=0.7, x=0.47)), row=1, col=1)
    fig.add_trace(go.Scatter(x=coord_data['lon'], y=coord_data['lat'], mode='markers',
                              marker=dict(size=6, color='black', opacity=0.6), text=coord_data['country'],
                              hovertemplate='<b>%{text}</b><br>Lat: %{y}<br>Lon: %{x}<extra></extra>'), row=1, col=1)
    fig.add_trace(go.Surface(x=grid_lon_mesh, y=grid_lat_mesh, z=grid_intensity, colorscale=color_scale,
                              showscale=False, opacity=0.8), row=1, col=2)
    # Configure 2D axes
    fig.update_xaxes(title_text='Longitude', row=1, col=1)
    fig.update_yaxes(title_text='Latitude', row=1, col=1)
    # Configure map layout
    if region_filter == "Nigeria":
        center_lat, center_lon = 9.0820, 8.6753; zoom = 5
    elif region_filter == "Africa":
        center_lat, center_lon = 0, 20; zoom = 2
    else:
        center_lat, center_lon = 20, 0; zoom = 1
    fig.update_layout(scene=dict(xaxis_title="Longitude", yaxis_title="Latitude", zaxis_title="Intensity",
                                camera=dict(eye=dict(x=1.2, y=1.2, z=0.8))),
                      margin=dict(l=0, r=0, t=60, b=0), height=600,
                      title=dict(text="Disease Outbreak Isoline Analysis", x=0.5,
                                 font=dict(size=18, color="#2c3e50")))
    st.plotly_chart(fig, use_container_width=True)
