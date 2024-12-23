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


def get_death_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate death rankings excluding specific servers"""
    deaths_df = dfs["deaths"]
    names_df = dfs["player_names"]

    death_counts = deaths_df.groupby("uuid").size().reset_index(name="deaths")
    death_ranking = death_counts.merge(names_df, on="uuid")
    death_ranking = death_ranking.sort_values("deaths", ascending=False)

    return death_ranking[["player_name", "deaths"]].to_dict("records")


def get_death_rate_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate average death rate (deaths per hour) for each player"""
    deaths_df = dfs["deaths"]
    sessions_df = dfs["sessions"]
    names_df = dfs["player_names"]

    death_counts = deaths_df.groupby("uuid").size().reset_index(name="total_deaths")

    play_time = sessions_df.groupby("uuid")["play_time"].sum().reset_index()
    play_time["play_hours"] = play_time["play_time"] / 3600
    play_time = play_time[play_time["play_hours"] >= 1]

    death_rate = death_counts.merge(play_time, on="uuid")
    death_rate["deaths_per_hour"] = (
        death_rate["total_deaths"] / death_rate["play_hours"]
    )
    death_rate = death_rate.merge(names_df, on="uuid")
    death_rate = death_rate.sort_values("deaths_per_hour", ascending=False)

    return [
        {
            "player_name": row["player_name"],
            "deaths_per_hour": round(row["deaths_per_hour"], 2),
            "total_deaths": int(row["total_deaths"]),
            "play_hours": round(row["play_hours"], 1),
        }
        for _, row in death_rate.iterrows()
    ]


def get_chat_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate player rankings by total message count"""
    messages_df = dfs["messages"]
    names_df = dfs["player_names"]

    message_counts = messages_df.groupby("uuid").size().reset_index(name="messages")
    chat_ranking = message_counts.merge(names_df, on="uuid")
    chat_ranking = chat_ranking.sort_values("messages", ascending=False)

    return chat_ranking[["player_name", "messages"]].to_dict("records")


def get_chat_rate_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate player rankings by messages per hour of playtime"""
    messages_df = dfs["messages"]
    sessions_df = dfs["sessions"]
    names_df = dfs["player_names"]

    message_counts = (
        messages_df.groupby("uuid").size().reset_index(name="total_messages")
    )

    play_time = sessions_df.groupby("uuid")["play_time"].sum().reset_index()
    play_time["play_hours"] = play_time["play_time"] / 3600
    play_time = play_time[play_time["play_hours"] >= 1]

    chat_rate = message_counts.merge(play_time, on="uuid")
    chat_rate["messages_per_hour"] = (
        chat_rate["total_messages"] / chat_rate["play_hours"]
    )
    chat_rate = chat_rate.merge(names_df, on="uuid")
    chat_rate = chat_rate.sort_values("messages_per_hour", ascending=False)

    return [
        {
            "player_name": row["player_name"],
            "messages_per_hour": round(row["messages_per_hour"], 2),
            "total_messages": int(row["total_messages"]),
            "play_hours": round(row["play_hours"], 1),
        }
        for _, row in chat_rate.iterrows()
    ]


def get_pvp_kill_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate player rankings by PvP kills"""
    deaths_df = dfs["deaths"]
    names_df = dfs["player_names"]

    # Filter deaths to only include PvP kills (where 'by' is a UUID)
    uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    pvp_deaths = deaths_df[deaths_df["by"].str.match(uuid_pattern, na=False)]

    # Count kills per killer UUID
    kill_counts = pvp_deaths.groupby("by").size().reset_index(name="kills")

    # Merge with player names (using 'by' as uuid)
    kill_ranking = kill_counts.merge(names_df, left_on="by", right_on="uuid")

    # Sort by kills descending
    kill_ranking = kill_ranking.sort_values("kills", ascending=False)

    # Convert to list of dicts
    result = kill_ranking[["player_name", "kills"]].to_dict("records")

    return result


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
