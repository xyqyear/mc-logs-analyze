import os

from overall_frames import (
    active_players,
    playtime_ranking,  # Add this import
    server_players,
    timeline,
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
    playtime_ranking.write_frame(dfs, FRAMES_DIR)  # Add this line


if __name__ == "__main__":
    main()
