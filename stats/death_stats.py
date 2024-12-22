import pandas as pd


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


def get_dangerous_server_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate most dangerous servers based on deaths per hour of playtime"""
    deaths_df = dfs["deaths"]
    sessions_df = dfs["sessions"]

    death_counts = (
        deaths_df.groupby("server_name").size().reset_index(name="total_deaths")
    )

    play_time = sessions_df.groupby("server_name")["play_time"].sum().reset_index()
    play_time["play_hours"] = play_time["play_time"] / 3600
    play_time = play_time[play_time["play_hours"] >= 1]

    danger_rate = death_counts.merge(play_time, on="server_name")
    danger_rate["deaths_per_hour"] = (
        danger_rate["total_deaths"] / danger_rate["play_hours"]
    )
    danger_rate = danger_rate.sort_values("deaths_per_hour", ascending=False)

    return [
        {
            "server_name": row["server_name"],
            "deaths_per_hour": round(row["deaths_per_hour"], 2),
            "total_deaths": int(row["total_deaths"]),
            "play_hours": round(row["play_hours"], 1),
        }
        for _, row in danger_rate.iterrows()
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
