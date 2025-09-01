from __future__ import annotations

from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Paths:
    DATA_CSV: str = "disease_outbreaks_HDX.csv"
    LOGO: str = "logo.png"

ALT_BASE_COLORS = {
    "Reds": "#d62728",
    "Blues": "#1f77b4",
    "Plasma": "#b63679",
    "Magma": "#fb9a99",
    "Turbo": "#c51b7d",
}

COLOR_THEME_OPTIONS: List[str] = [
    "Reds", "Blues", "Plasma", "Magma", "Turbo",
]
