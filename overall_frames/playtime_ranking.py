from stats import get_playtime_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the playtime ranking frame"""
    rankings = get_playtime_ranking(dfs)
    top_players = rankings[:10]  # Show top 10

    content = [
        "\\begin{frame}{游玩时间排名}",
        "\\begin{center}",
        "\\begin{tabular}{lr}",
        "\\toprule",
        "玩家 & 游玩时长(小时) \\\\",
        "\\midrule",
    ]

    # Add each player's data with thousand separator and one decimal place
    for rank in top_players:
        player_name = escape_latex(rank["player_name"])
        content.append(f"{player_name} & {rank['play_hours']:,.1f} \\\\")

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/playtime_ranking.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
