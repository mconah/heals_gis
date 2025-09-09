from __future__ import annotations

from dataclasses import dataclass
from typing import List
from neon_api import NeonAPI

neon = NeonAPI(api_key="napi_mgvr1mz1fm3uywv7ullwl7dokpz62dyw5287ggbu8za5j04kg2c9xwdfbv6h22cp")

@dataclass(frozen=True)
class Paths:
    DATA_CSV: str = "disease_outbreaks_HDX.csv"
    LOGO: str = "logo.png"

NEON_DB_CONFIG = {
    "project_id": "polished-meadow-24726115",
    "branch_id": "br-wandering-queen-ab8q5oi7",
    "database": "gs",
    "user": "neondb_owner",
    "password": "npg_SBXuCaUgE50l",
    "table": "outbreaks"
}

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
