from stats import get_chat_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the chat ranking frame"""
    rankings = get_chat_ranking(dfs)
    top_players = rankings[:10]  # Show top 10

    content = [
        "\\begin{frame}{聊天排行}",
        "\\begin{center}",
        "\\begin{tabular}{lr}",
        "\\toprule",
        "玩家 & 消息数量 \\\\",
        "\\midrule",
    ]

    for rank in top_players:
        player_name = escape_latex(rank["player_name"])
        content.append(f"{player_name} & {rank['messages']:,} \\\\")

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/chat_ranking.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
