from stats import (
    get_active_players,
    get_advancement_ranking,
    get_chat_ranking,
    get_chat_rate_ranking,
    get_daily_playtime,
    get_dangerous_server_ranking,
    get_death_ranking,
    get_death_rate_ranking,
    get_hourly_playtime,
    get_peak_concurrent_players,
    get_playtime_ranking,
    get_pvp_kill_ranking,
    get_server_chat_ranking,
    get_server_chat_rate_ranking,
    get_server_player_list,  # Update this line
    get_server_playtime_ranking,  # Add this import
    get_server_timeline,
    get_server_variety_ranking,
    get_total_advancements,
    get_total_deaths,
    get_total_messages,
    get_total_playtime,
    get_weekday_playtime,
)
from stats.common import load_dataframes


def main():
    """Main function to generate all statistics"""
    dfs = load_dataframes()

    # Generate server timeline
    timeline = get_server_timeline(dfs)
    print("\nServer Timeline:")
    for server in timeline:
        print(
            f"{server['server_name']}: created at {server['created_at']}, closed at {server['closed_at']}"
        )

    # Generate total playtime
    total_play = get_total_playtime(dfs)
    print("\nTotal Server Playtime:")
    print(f"{total_play['total_hours']} hours ({total_play['total_days']} days)")

    # Generate active players list
    active_players = get_active_players(dfs)
    print("\nActive Players:")
    print(f"Total: {len(active_players)} players")
    for player in active_players:
        print(f"- {player['player_name']}")

    # Generate playtime rankings
    playtime_ranking = get_playtime_ranking(dfs)
    print("\nMost Active Players:")
    for rank in playtime_ranking[:10]:
        print(f"{rank['player_name']}: {rank['play_hours']} hours")

    # Generate server variety rankings
    server_variety_ranking = get_server_variety_ranking(dfs)
    print("\nMost Server Variety:")
    for rank in server_variety_ranking[:10]:
        print(f"{rank['player_name']}: {rank['server_count']} different servers")

    # Generate death rankings
    death_ranking = get_death_ranking(dfs)
    print("\nDeath Rankings:")
    for rank in death_ranking[:10]:
        print(f"{rank['player_name']}: {rank['deaths']} deaths")

    # Generate death rate rankings
    death_rate_ranking = get_death_rate_ranking(dfs)
    print("\nDeath Rate Rankings (deaths per hour):")
    for rank in death_rate_ranking[:10]:
        print(
            f"{rank['player_name']}: {rank['deaths_per_hour']} deaths/hour "
            f"({rank['total_deaths']} deaths in {rank['play_hours']} hours)"
        )

    # Generate dangerous server rankings
    dangerous_servers = get_dangerous_server_ranking(dfs)
    print("\nMost Dangerous Servers (deaths per hour):")
    for rank in dangerous_servers:
        print(
            f"{rank['server_name']}: {rank['deaths_per_hour']} deaths/hour "
            f"({rank['total_deaths']} deaths in {rank['play_hours']} hours)"
        )

    # Generate chat rankings
    chat_ranking = get_chat_ranking(dfs)
    print("\nMost Talkative Players:")
    for rank in chat_ranking[:10]:
        print(f"{rank['player_name']}: {rank['messages']} messages")

    # Generate chat rate rankings
    chat_rate_ranking = get_chat_rate_ranking(dfs)
    print("\nChattiest Players (messages per hour):")
    for rank in chat_rate_ranking[:10]:
        print(
            f"{rank['player_name']}: {rank['messages_per_hour']} messages/hour "
            f"({rank['total_messages']} messages in {rank['play_hours']} hours)"
        )

    # Generate server chat rankings
    server_chat_ranking = get_server_chat_ranking(dfs)
    print("\nMost Talkative Servers:")
    for rank in server_chat_ranking:
        print(f"{rank['server_name']}: {rank['messages']} messages")

    # Generate server chat rate rankings
    server_chat_rate_ranking = get_server_chat_rate_ranking(dfs)
    print("\nNoisiest Servers (messages per hour):")
    for rank in server_chat_rate_ranking:
        print(
            f"{rank['server_name']}: {rank['messages_per_hour']} messages/hour "
            f"({rank['total_messages']} messages in {rank['play_hours']} hours)"
        )

    # Generate PvP kill rankings
    pvp_kill_ranking = get_pvp_kill_ranking(dfs)
    print("\nTop PvP Killers:")
    for rank in pvp_kill_ranking[:10]:
        print(f"{rank['player_name']}: {rank['kills']} kills")

    # Generate advancement rankings
    advancement_ranking = get_advancement_ranking(dfs)
    print("\nMost Achievements Earned:")
    for rank in advancement_ranking[:10]:
        print(f"{rank['player_name']}: {rank['advancements']} advancements")

    # Generate total advancements count
    total_advancements = get_total_advancements(dfs)
    print(f"\nTotal Advancements Earned: {total_advancements['total_advancements']}")

    # Generate total deaths count
    total_deaths = get_total_deaths(dfs)
    print(f"\nTotal Deaths: {total_deaths['total_deaths']}")

    # Generate server player counts
    server_players = get_server_player_list(dfs)
    print("\nPlayers per Server:")
    for stat in server_players:
        print(f"\n{stat['server_name']}: {stat['player_count']} players")
        print("Players:", ", ".join(stat["player_list"]))

    # Generate peak concurrent players
    peak_concurrent = get_peak_concurrent_players(dfs)
    print("\nPeak Concurrent Players by Server:")
    for stat in peak_concurrent:
        print(f"\n{stat['server_name']}:")
        print(f"Peak: {stat['peak_players']} players at {stat['peak_time']}")
        print("Players online:", ", ".join(stat["player_list"]))

    # Calculate total messages sent
    total_messages = get_total_messages(dfs)
    print(f"\nTotal Messages Sent: {total_messages['total_messages']}")

    # Generate daily playtime statistics
    daily_playtime = get_daily_playtime(dfs)
    print("\nDaily Playtime Sample (first 5 days):")
    for day in daily_playtime[:5]:
        print(f"{day['date']}: {day['play_hours']} hours")

    # Generate weekday playtime statistics
    weekday_playtime = get_weekday_playtime(dfs)
    print("\nPlaytime by Day of Week:")
    for day in weekday_playtime:
        print(f"{day['weekday']}: {day['play_hours']} hours")

    # Generate hourly playtime statistics
    hourly_playtime = get_hourly_playtime(dfs)
    print("\nPlaytime by Hour of Day:")
    for hour in hourly_playtime:
        print(f"{hour['hour']}: {hour['play_hours']} hours")

    # Generate server playtime rankings
    server_playtime = get_server_playtime_ranking(dfs)
    print("\nServer Playtime Rankings:")
    for rank in server_playtime:
        print(
            f"{rank['server_name']}: {rank['play_hours']} hours "
            f"({rank['play_days']} days)"
        )


if __name__ == "__main__":
    main()
