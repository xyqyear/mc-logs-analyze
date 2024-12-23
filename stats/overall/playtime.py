import pandas as pd


def get_total_playtime(dfs: dict[str, pd.DataFrame]) -> dict:
    """Calculate total playtime across all players"""
    sessions_df = dfs["sessions"]

    # Sum up all playtime and convert to hours
    total_seconds = sessions_df["play_time"].sum()
    total_hours = total_seconds / 3600

    return {
        "total_hours": round(total_hours, 1),
        "total_days": round(total_hours / 24, 1),
    }


def get_active_players(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Get list of all players who have logged in at least once"""
    sessions_df = dfs["sessions"]
    names_df = dfs["player_names"]

    # Get unique UUIDs from sessions
    active_uuids = sessions_df["uuid"].unique()

    # Get player names for active UUIDs
    active_players = names_df[names_df["uuid"].isin(active_uuids)]

    # Sort by player name
    active_players = active_players.sort_values("player_name")

    # Convert to list of dicts
    result = [{"player_name": name} for name in active_players["player_name"]]

    return result
