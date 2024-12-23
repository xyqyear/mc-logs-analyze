from stats import get_death_rate_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the death rate ranking frame"""
    rankings = get_death_rate_ranking(dfs)
    top_players = rankings[:10]  # Show top 10

    content = [
        "\\begin{frame}{平均死亡排行}",
        "\\small{（死亡次数除以游玩时间）（总游玩时间一小时以下除外）}",
        "\\begin{center}",
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "玩家 & 每小时死亡次数 & 总死亡次数 \\\\",
        "\\midrule",
    ]

    # Add each player's data
    for rank in top_players:
        player_name = escape_latex(rank["player_name"])
        content.append(
            f"{player_name} & {rank['deaths_per_hour']:.1f} & {rank['total_deaths']:,} \\\\"
        )

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/death_rate_ranking.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
