import pandas as pd


def get_server_chat_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate server rankings by total message count"""
    messages_df = dfs["messages"]

    # Count messages per server
    message_counts = (
        messages_df.groupby("server_name").size().reset_index(name="messages")
    )

    # Sort by message count descending
    server_ranking = message_counts.sort_values("messages", ascending=False)

    # Convert to list of dicts
    result = server_ranking[["server_name", "messages"]].to_dict("records")

    return result


def get_server_chat_rate_ranking(dfs: dict[str, pd.DataFrame]) -> list[dict]:
    """Calculate server rankings by messages per hour of playtime"""
    messages_df = dfs["messages"]
    sessions_df = dfs["sessions"]

    # Count messages per server
    message_counts = (
        messages_df.groupby("server_name").size().reset_index(name="total_messages")
    )

    # Calculate total play time in hours per server
    play_time = sessions_df.groupby("server_name")["play_time"].sum().reset_index()
    play_time["play_hours"] = play_time["play_time"] / 3600

    # Filter out servers with less than 1 hour total playtime
    play_time = play_time[play_time["play_hours"] >= 1]

    # Merge messages and play time
    chat_rate = message_counts.merge(play_time, on="server_name")
    chat_rate["messages_per_hour"] = (
        chat_rate["total_messages"] / chat_rate["play_hours"]
    )

    # Sort by message rate descending
    chat_rate = chat_rate.sort_values("messages_per_hour", ascending=False)

    # Convert to list of dicts with rounded values
    result = [
        {
            "server_name": row["server_name"],
            "messages_per_hour": round(row["messages_per_hour"], 2),
            "total_messages": int(row["total_messages"]),
            "play_hours": round(row["play_hours"], 1),
        }
        for _, row in chat_rate.iterrows()
    ]

    return result
