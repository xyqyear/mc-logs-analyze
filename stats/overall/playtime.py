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


def get_daily_playtime(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate total playtime for each day of the year in UTC+8, handling cross-day sessions"""
    sessions_df = dfs["sessions"]

    # Convert timestamps to pandas timestamps in UTC+8
    sessions_df["start_time"] = pd.to_datetime(
        sessions_df["join_timestamp"], unit="s", utc=True
    ).dt.tz_convert("Asia/Shanghai")
    sessions_df["end_time"] = sessions_df["start_time"] + pd.to_timedelta(
        sessions_df["play_time"], unit="s"
    )

    # Initialize list to store daily segments
    daily_segments = []

    for _, session in sessions_df.iterrows():
        start = session["start_time"]
        end = session["end_time"]
        current = start.normalize()  # Get start of day

        while current < end:
            next_day = current + pd.Timedelta(days=1)
            segment_end = min(end, next_day)
            segment_duration = (segment_end - max(start, current)).total_seconds()

            if segment_duration > 0:
                daily_segments.append(
                    {"date": current.date(), "play_time": segment_duration}
                )

            current = next_day

    # Convert segments to DataFrame and group by date
    segments_df = pd.DataFrame(daily_segments)
    if len(segments_df) > 0:
        daily_play = segments_df.groupby("date")["play_time"].sum().reset_index()
        daily_play["play_hours"] = daily_play["play_time"] / 3600

        # Ensure all days between first and last session are included
        start_date = daily_play["date"].min()
        end_date = daily_play["date"].max()
        all_dates = pd.date_range(start=start_date, end=end_date, freq="D").date

        # Create complete date index with 0 hours for missing days
        daily_hours = pd.DataFrame({"date": all_dates})
        daily_hours = daily_hours.merge(
            daily_play[["date", "play_hours"]], on="date", how="left"
        ).fillna(0)
    else:
        # Handle case with no valid sessions
        daily_hours = pd.DataFrame(columns=["date", "play_hours"])

    # Convert to list of dicts
    result = [
        {
            "date": row["date"].isoformat(),
            "play_hours": round(row["play_hours"], 1),
        }
        for _, row in daily_hours.iterrows()
    ]

    return result


def get_weekday_playtime(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate total playtime for each day of the week in UTC+8"""
    sessions_df = dfs["sessions"]

    # Convert timestamps to pandas timestamps in UTC+8
    sessions_df["start_time"] = pd.to_datetime(sessions_df["join_timestamp"], unit="s", utc=True).dt.tz_convert("Asia/Shanghai")
    sessions_df["end_time"] = sessions_df["start_time"] + pd.to_timedelta(sessions_df["play_time"], unit="s")

    # Initialize list to store daily segments
    weekday_segments = []

    for _, session in sessions_df.iterrows():
        start = session["start_time"]
        end = session["end_time"]
        current = start.normalize()  # Get start of day

        while current < end:
            next_day = current + pd.Timedelta(days=1)
            segment_end = min(end, next_day)
            segment_duration = (segment_end - max(start, current)).total_seconds()

            if segment_duration > 0:
                weekday_segments.append({
                    "weekday": current.weekday(),
                    "play_time": segment_duration
                })

            current = next_day

    # Convert segments to DataFrame and group by weekday
    segments_df = pd.DataFrame(weekday_segments)
    if len(segments_df) > 0:
        weekday_play = segments_df.groupby("weekday")["play_time"].sum().reset_index()
        weekday_play["play_hours"] = weekday_play["play_time"] / 3600

        # Create dict for weekday names
        weekday_names = {
            0: "Monday",
            1: "Tuesday", 
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

        # Convert to list of dicts with weekday names
        result = [
            {
                "weekday": weekday_names[row["weekday"]],
                "play_hours": round(row["play_hours"], 1)
            }
            for _, row in weekday_play.iterrows()
        ]

        # Sort by weekday order
        result = sorted(result, key=lambda x: list(weekday_names.values()).index(x["weekday"]))
    else:
        # Handle case with no valid sessions
        result = [
            {"weekday": day, "play_hours": 0.0}
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        ]

    return result
