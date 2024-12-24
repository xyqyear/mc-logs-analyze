from stats import get_server_chat_rate_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the server chat rate ranking frame"""
    rankings = get_server_chat_rate_ranking(dfs)

    content = [
        "\\begin{frame}{各服务器聊天活跃度}",
        "\\begin{center}",
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "服务器 & 聊天频率 & 总发言数 \\\\",
        "\\midrule",
    ]

    for rank in rankings:
        server_name = escape_latex(rank["server_name"])
        content.append(
            f"{server_name} & {rank['messages_per_hour']:.1f} 条/小时 & {rank['total_messages']:,} \\\\"
        )

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/server_chat_rate_ranking.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
