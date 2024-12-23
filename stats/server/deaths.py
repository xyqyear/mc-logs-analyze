import pandas as pd


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
