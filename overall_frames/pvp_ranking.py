from stats import get_pvp_kill_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the PvP kill ranking frame"""
    rankings = get_pvp_kill_ranking(dfs)
    top_players = rankings[:10]  # Show top 10

    content = [
        "\\begin{frame}{杀人最多的玩家}",
        "\\small{（不包含枪战小游戏）}",
        "\\begin{center}",
        "\\begin{tabular}{lr}",
        "\\toprule",
        "玩家 & 击杀数 \\\\",
        "\\midrule",
    ]

    # Add each player's data
    for rank in top_players:
        player_name = escape_latex(rank["player_name"])
        content.append(f"{player_name} & {rank['kills']:,} \\\\")

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/pvp_ranking.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
