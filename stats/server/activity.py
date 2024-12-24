from datetime import datetime

import pandas as pd


def get_peak_concurrent_players(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Find peak concurrent players for each server"""
    sessions_df = dfs["sessions"]
    names_df = dfs["player_names"]

    results = []

    for server_name in sessions_df["server_name"].unique():
        server_sessions = sessions_df[sessions_df["server_name"] == server_name]

        # Create events list with joins and quits
        events = []
        for _, session in server_sessions.iterrows():
            join_time = pd.to_datetime(session["join_timestamp"], unit="s")
            quit_time = join_time + pd.Timedelta(seconds=session["play_time"])
            events.append({"time": join_time, "change": 1, "uuid": session["uuid"]})
            events.append({"time": quit_time, "change": -1, "uuid": session["uuid"]})

        events = sorted(events, key=lambda x: x["time"])

        # Track concurrent players
        current_count = 0
        peak_count = 0
        peak_time: datetime | None = None
        peak_players = set()
        current_players = set()

        for event in events:
            if event["change"] == 1:
                current_players.add(event["uuid"])
            else:
                current_players.discard(event["uuid"])

            current_count = len(current_players)

            if current_count > peak_count:
                peak_count = current_count
                peak_time = event["time"]
                peak_players = current_players.copy()

        if peak_time:
            # Convert UTC to UTC+8
            peak_time_utc8 = peak_time + pd.Timedelta(hours=8)

            # Get player names for peak players
            peak_player_names = names_df[names_df["uuid"].isin(peak_players)]
            player_list = peak_player_names["player_name"].tolist()

            results.append(
                {
                    "server_name": server_name,
                    "peak_players": peak_count,
                    "peak_time": peak_time_utc8.strftime("%Y-%m-%d %H:%M:%S"),
                    "player_list": sorted(player_list),
                }
            )

    # Sort by peak player count descending
    results = sorted(results, key=lambda x: x["peak_players"], reverse=True)

    return results


def get_server_timeline(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Get timeline of server creations based on actual player activity"""
    sessions_df = dfs["sessions"]

    # Group by server and find first join
    first_joins = sessions_df.groupby("server_name")["join_timestamp"].min()

    # Calculate last quit time for each server
    last_quits = sessions_df.groupby("server_name").apply(
        lambda group: (group["join_timestamp"] + group["play_time"]).max()
    )

    # Create timeline dataframe
    timeline = pd.DataFrame(
        {
            "server_name": first_joins.index,
            "created_time": pd.to_datetime(first_joins, unit="s"),
            "closed_time": pd.to_datetime(last_quits, unit="s"),
        }
    )

    # Convert to UTC+8
    timeline["created_time"] = timeline["created_time"] + pd.Timedelta(hours=8)
    timeline["closed_time"] = timeline["closed_time"] + pd.Timedelta(hours=8)

    # Sort by creation time
    timeline = timeline.sort_values("created_time")

    # Format output
    result = [
        {
            "server_name": row["server_name"],
            "created_at": row["created_time"].strftime("%Y-%m-%d %H:%M:%S"),
            "closed_at": row["closed_time"].strftime("%Y-%m-%d %H:%M:%S"),
        }
        for _, row in timeline.iterrows()
    ]

    return result


def get_server_player_list(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Get list of unique players for each server with their names"""
    sessions_df = dfs["sessions"]
    names_df = dfs["player_names"]

    # Get unique player-server combinations
    server_players = sessions_df.groupby("server_name")["uuid"].unique().reset_index()

    # Process each server
    result = []
    for _, row in server_players.iterrows():
        # Get player names for this server's UUIDs
        server_uuids = row["uuid"]
        player_names = sorted(
            names_df[names_df["uuid"].isin(server_uuids)]["player_name"].unique()
        )

        result.append(
            {
                "server_name": row["server_name"],
                "player_count": len(player_names),
                "player_list": player_names,
            }
        )

    # Sort by player count descending
    result.sort(key=lambda x: x["player_count"], reverse=True)

    return result
