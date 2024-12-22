import pandas as pd


def get_playtime_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate player rankings by total play time"""
    sessions_df = dfs["sessions"]
    names_df = dfs["player_names"]

    # Calculate total play time in hours per player
    play_time = sessions_df.groupby("uuid")["play_time"].sum().reset_index()
    play_time["play_hours"] = play_time["play_time"] / 3600

    # Merge with player names
    playtime_ranking = play_time.merge(names_df, on="uuid")

    # Sort by play time descending
    playtime_ranking = playtime_ranking.sort_values("play_hours", ascending=False)

    # Convert to list of dicts with rounded values
    result = [
        {
            "player_name": row["player_name"],
            "play_hours": round(row["play_hours"], 1),
        }
        for _, row in playtime_ranking.iterrows()
    ]

    return result


def get_server_variety_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate player rankings by number of different servers played on"""
    sessions_df = dfs["sessions"]
    names_df = dfs["player_names"]

    # Count unique servers per player
    unique_servers = (
        sessions_df.groupby("uuid")["server_name"]
        .nunique()
        .reset_index(name="server_count")
    )

    # Merge with player names
    variety_ranking = unique_servers.merge(names_df, on="uuid")

    # Sort by server count descending
    variety_ranking = variety_ranking.sort_values("server_count", ascending=False)

    # Convert to list of dicts
    result = [
        {
            "player_name": row["player_name"],
            "server_count": int(row["server_count"]),
        }
        for _, row in variety_ranking.iterrows()
    ]

    return result


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


def get_server_player_counts(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Get count of unique players for each server"""
    sessions_df = dfs["sessions"]

    # Count unique players (UUIDs) per server
    player_counts = (
        sessions_df.groupby("server_name")["uuid"]
        .nunique()
        .reset_index(name="player_count")
    )

    # Sort by player count descending
    player_counts = player_counts.sort_values("player_count", ascending=False)

    # Convert to list of dicts
    result = [
        {
            "server_name": row["server_name"],
            "player_count": int(row["player_count"]),
        }
        for _, row in player_counts.iterrows()
    ]

    return result


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
