import pandas as pd


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
