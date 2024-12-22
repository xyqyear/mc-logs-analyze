from stats import (
    get_active_players,
    get_advancement_ranking,
    get_chat_ranking,
    get_chat_rate_ranking,
    get_dangerous_server_ranking,
    get_death_ranking,
    get_death_rate_ranking,
    get_playtime_ranking,
    get_pvp_kill_ranking,
    get_server_chat_ranking,
    get_server_chat_rate_ranking,
    get_server_player_counts,
    get_server_variety_ranking,
    get_total_playtime,
)
from stats.common import load_dataframes


def main():
    """Main function to generate all statistics"""
    dfs = load_dataframes()

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

    # Generate server player counts
    server_players = get_server_player_counts(dfs)
    print("\nPlayers per Server:")
    for stat in server_players:
        print(f"{stat['server_name']}: {stat['player_count']} players")


if __name__ == "__main__":
    main()
