import os

from overall_frames import (
    active_players,
    daily_playtime,
    dangerous_servers,
    death_ranking,
    death_rate_ranking,
    peak_players,
    playtime_ranking,
    pvp_ranking,  # Add this import
    server_players,
    server_playtime,
    time_distribution,
    timeline,
    total_deaths,
    total_playtime,
    variety_ranking,
)
from stats.common import load_dataframes

FRAMES_DIR = "representation-overall/frames"
FIGURES_DIR = "representation-overall/figures"


def ensure_dirs():
    """Ensure all required directories exist"""
    for dir_path in [FRAMES_DIR, FIGURES_DIR]:
        os.makedirs(dir_path, exist_ok=True)


def main():
    """Main function to generate all TeX files"""
    dfs = load_dataframes()

    # Ensure directories exist first
    ensure_dirs()

    # Generate all frames
    timeline.create_figure(dfs, FIGURES_DIR)
    timeline.write_frame(FRAMES_DIR)
    active_players.write_frame(dfs, FRAMES_DIR)
    server_players.write_frame(dfs, FRAMES_DIR)
    variety_ranking.write_frame(dfs, FRAMES_DIR)
    total_playtime.write_frame(dfs, FRAMES_DIR)
    server_playtime.write_frame(dfs, FRAMES_DIR)  # Add this line
    playtime_ranking.write_frame(dfs, FRAMES_DIR)
    daily_playtime.create_figure(dfs, FIGURES_DIR)
    daily_playtime.write_frame(FRAMES_DIR)
    time_distribution.create_weekday_figure(dfs, FIGURES_DIR)
    time_distribution.create_hourly_figure(dfs, FIGURES_DIR)
    time_distribution.write_frames(FRAMES_DIR)

    # Update peak players to only write frame
    peak_players.write_frame(dfs, FRAMES_DIR)
    total_deaths.write_frame(dfs, FRAMES_DIR)
    death_ranking.write_frame(dfs, FRAMES_DIR)
    death_rate_ranking.write_frame(dfs, FRAMES_DIR)
    dangerous_servers.write_frame(dfs, FRAMES_DIR)  # Add this line
    pvp_ranking.write_frame(dfs, FRAMES_DIR)  # Add this line


if __name__ == "__main__":
    main()
