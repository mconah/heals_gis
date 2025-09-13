from __future__ import annotations

import pandas as pd
import streamlit as st
from .config import Paths, neon, NEON_DB_CONFIG
from sqlalchemy import create_engine


def load_data(csv_path: str | None = None, use_db: bool = True, force_refresh: bool = False) -> pd.DataFrame:
    """Load and normalize the outbreaks data with caching.

    Uses Streamlit session state to cache data and avoid repeated database queries.
    Data is only reloaded when force_refresh=True or when data is not in cache.
    
    Args:
        csv_path: Path to CSV file (fallback option)
        use_db: Whether to use database (currently always True)
        force_refresh: If True, bypass cache and reload data from database
    
    Returns:
        Pandas DataFrame with outbreak data
    
    Raises:
        Exception: If both database and CSV loading fail
    """
    # Check if data is cached and force_refresh is not requested
    if not force_refresh and 'cached_data' in st.session_state:
        return st.session_state.cached_data
    
    df = None
    error_msg = None
    
    # Try to load data from database first
    try:
        conn_string = "postgresql://neondb_owner:npg_SBXuCaUgE50l@ep-little-truth-abzgs476-pooler.eu-west-2.aws.neon.tech/gs?sslmode=require&channel_binding=require"
        sqlalchemy_conn = f"postgresql+psycopg://{conn_string.split('://', 1)[1]}"
        engine = create_engine(sqlalchemy_conn)
        df = pd.read_sql_query("SELECT * FROM outbreaks", engine)
        st.session_state.data_source = "database"
        
    except Exception as e:
        error_msg = f"Database connection failed: {str(e)}"
        st.session_state.data_source = "error"
        
        # Try fallback to CSV if available
        if csv_path or Paths.DATA_CSV:
            try:
                path = csv_path or Paths.DATA_CSV
                df = pd.read_csv(path)
                st.session_state.data_source = "csv"
                error_msg = None  # Clear error since CSV worked
            except Exception as csv_e:
                error_msg += f"\nCSV fallback also failed: {str(csv_e)}"
    
    # If no data could be loaded, create a dummy dataset or raise error
    if df is None:
        # For demo purposes, create a minimal dummy dataset
        st.error(f"**Data Loading Failed**\n\n{error_msg}")
        st.info("**Troubleshooting:**\n- Check your internet connection\n- Verify database credentials\n- Ensure CSV file exists if using fallback")
        
        # Create minimal dummy data to prevent app crash
        df = pd.DataFrame({
            'year': [2020, 2021, 2022],
            'disease': ['Sample Disease 1', 'Sample Disease 2', 'Sample Disease 3'],
            'country': ['Nigeria', 'Ghana', 'Kenya'],
            'iso3': ['NGA', 'GHA', 'KEN'],
            'icd10n': ['Category 1', 'Category 2', 'Category 3'],
            'unsd_region': ['Africa', 'Africa', 'Africa'],
            'unsd_subregion': ['Sub-Saharan Africa', 'Sub-Saharan Africa', 'Sub-Saharan Africa'],
            'who_region': ['African Region', 'African Region', 'African Region'],
            'DONs': ['DON001', 'DON002', 'DON003']
        })
        st.session_state.data_source = "dummy"
        st.warning("Using dummy data for demonstration. Please fix data connection.")
    
    # Clean and normalize data
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(int)
    
    # Cache the data in session state
    st.session_state.cached_data = df
    
    return df 

def years_sorted(df: pd.DataFrame) -> list[int]:
    ys = sorted(df["year"].dropna().unique().tolist(), reverse=True)
    return ys


def filter_df(
    df: pd.DataFrame,
    years: list[int],
    category: str | None = None,
    diseases: list[str] | None = None,
) -> pd.DataFrame:
    out = df[df["year"].isin(years)]
    if category and category != "All":
        out = out[out["icd10n"] == category]
    if diseases:
        out = out[out["disease"].isin(diseases)]
    return out
