from pathlib import Path

import pandas as pd


def load_dataframes():
    """Load all dataframes from CSV files"""
    base_path = Path("data")
    return {
        "deaths": pd.read_csv(base_path / "deaths.csv"),
        "servers": pd.read_csv(base_path / "servers.csv"),
        "sessions": pd.read_csv(base_path / "sessions.csv"),
        "messages": pd.read_csv(base_path / "messages.csv"),
        "advancements": pd.read_csv(base_path / "advancements.csv"),
        "player_names": pd.read_csv(base_path / "player_names.csv"),
    }
