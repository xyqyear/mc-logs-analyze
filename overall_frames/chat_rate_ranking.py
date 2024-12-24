from stats import get_chat_rate_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the chat rate ranking frame"""
    rankings = get_chat_rate_ranking(dfs)
    top_players = rankings[:10]  # Show top 10

    content = [
        "\\begin{frame}{聊天频率排行}",
        "\\begin{center}",
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "玩家 & 聊天频率 & 总发言数 \\\\",
        "\\midrule",
    ]

    for rank in top_players:
        player_name = escape_latex(rank["player_name"])
        content.append(
            f"{player_name} & {rank['messages_per_hour']:.1f} 条/小时 & {rank['total_messages']:,} \\\\"
        )

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/chat_rate_ranking.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
