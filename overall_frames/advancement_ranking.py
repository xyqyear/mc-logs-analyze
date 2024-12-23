from stats import get_advancement_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the advancement ranking frame"""
    rankings = get_advancement_ranking(dfs)
    top_players = rankings[:10]  # Show top 10

    content = [
        "\\begin{frame}{获得成就排行}",
        "\\begin{center}",
        "\\begin{tabular}{lr}",
        "\\toprule",
        "玩家 & 成就数量 \\\\",
        "\\midrule",
    ]

    # Add each player's data
    for rank in top_players:
        player_name = escape_latex(rank["player_name"])
        content.append(f"{player_name} & {rank['advancements']:,} \\\\")

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/advancement_ranking.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
