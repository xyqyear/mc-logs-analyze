from stats import get_server_variety_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the server variety ranking frame"""
    # Get top players by server variety
    variety_data = get_server_variety_ranking(dfs)
    top_players = variety_data[:10]  # Show top 10

    content = [
        "\\begin{frame}{游玩服务器种类最多的玩家}",
        "\\begin{center}",
        "\\begin{tabular}{lr}",
        "\\toprule",
        "玩家 & 游玩服务器数量 \\\\",
        "\\midrule",
    ]

    # Add each player's data
    for rank in top_players:
        player_name = escape_latex(rank["player_name"])
        content.append(f"{player_name} & {rank['server_count']} \\\\")

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/variety_ranking.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
