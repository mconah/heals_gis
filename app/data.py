from __future__ import annotations

import pandas as pd
from .config import Paths


def load_data(csv_path: str | None = None) -> pd.DataFrame:
    """Load and normalize the outbreaks CSV.

    - Coerce Year to int
    - Drop rows with null Year
    """
    path = csv_path or Paths.DATA_CSV
    df = pd.read_csv(path)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = df["Year"].astype(int)
    return df


def years_sorted(df: pd.DataFrame) -> list[int]:
    ys = sorted(df["Year"].dropna().unique().tolist(), reverse=True)
    return ys


def filter_df(
    df: pd.DataFrame,
    years: list[int],
    category: str | None = None,
    diseases: list[str] | None = None,
) -> pd.DataFrame:
    out = df[df["Year"].isin(years)]
    if category and category != "All":
        out = out[out["icd10n"] == category]
    if diseases:
        out = out[out["Disease"].isin(diseases)]
    return out
