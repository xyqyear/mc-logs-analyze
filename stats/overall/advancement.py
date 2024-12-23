import pandas as pd


def get_total_advancements(dfs: dict[str, pd.DataFrame]) -> dict:
    """Calculate total advancements earned across all players"""
    advancements_df = dfs["advancements"]

    # Count total advancements
    total_count = len(advancements_df)

    return {"total_advancements": int(total_count)}
