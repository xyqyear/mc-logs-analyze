from stats import get_active_players

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the active players frame"""
    # Get and process player data
    active_players_data = get_active_players(dfs)
    active_players = sorted(player["player_name"] for player in active_players_data)
    active_players = [escape_latex(player) for player in active_players]

    # Split into columns
    num_cols = 4
    col_size = len(active_players) // num_cols + (len(active_players) % num_cols > 0)
    columns = [
        active_players[i : i + col_size]
        for i in range(0, len(active_players), col_size)
    ]

    # Generate content
    content = [
        "\\begin{frame}{活跃玩家}",
        "\\begin{center}",
        f"总计 {len(active_players)} 位玩家上线至少一次",
        "\\vspace{0.5em}",
        "\\begin{columns}[T]",
    ]

    for col in columns:
        content.extend(
            [
                f"\\begin{{column}}{{{1/num_cols}\\textwidth}}",
                "\\begin{itemize}\\setlength{\\itemsep}{0pt}\\tiny",
            ]
        )
        content.extend([f"\\item {player}" for player in col])
        content.extend(["\\end{itemize}", "\\end{column}"])

    content.extend(["\\end{columns}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/active_players.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
