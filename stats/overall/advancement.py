import pandas as pd


def get_total_advancements(dfs: dict[str, pd.DataFrame]) -> dict:
    """Calculate total advancements earned across all players"""
    advancements_df = dfs["advancements"]

    # Count total advancements
    total_count = len(advancements_df)

    return {"total_advancements": int(total_count)}


def get_advancement_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate player rankings by total advancements achieved"""
    advancements_df = dfs["advancements"]
    names_df = dfs["player_names"]

    # Count advancements per UUID
    advancement_counts = (
        advancements_df.groupby("uuid").size().reset_index(name="advancements")
    )

    # Merge with player names
    advancement_ranking = advancement_counts.merge(names_df, on="uuid")

    # Sort by advancement count descending
    advancement_ranking = advancement_ranking.sort_values(
        "advancements", ascending=False
    )

    # Convert to list of dicts
    result = advancement_ranking[["player_name", "advancements"]].to_dict("records")

    return result
