from __future__ import annotations

import pandas as pd
from .config import Paths, neon, NEON_DB_CONFIG
from sqlalchemy import create_engine


def load_data(csv_path: str | None = None, use_db: bool = True) -> pd.DataFrame:
    """Load and normalize the outbreaks CSV.

    - Coerce Year to int
    - Drop rows with null Year
    
    path = csv_path or Paths.DATA_CSV
    df = pd.read_csv(path)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = df["Year"].astype(int)
    return df
    """
    try:
        conn_string = "postgresql://neondb_owner:npg_SBXuCaUgE50l@ep-little-truth-abzgs476-pooler.eu-west-2.aws.neon.tech/gs?sslmode=require&channel_binding=require"
        sqlalchemy_conn = f"postgresql+psycopg://{conn_string.split('://', 1)[1]}"
        engine = create_engine(sqlalchemy_conn)
        df = pd.read_sql_query("SELECT * FROM outbreaks", engine)
    
    except Exception as e:
        print(f"Error loading from DB: {e}")
    
    print(df.info())
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(int)
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
