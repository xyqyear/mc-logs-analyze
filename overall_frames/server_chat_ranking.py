from stats import get_server_chat_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the server chat ranking frame"""
    rankings = get_server_chat_ranking(dfs)

    content = [
        "\\begin{frame}{每个服务器聊天数排行}",
        "\\begin{center}",
        "\\begin{tabular}{lr}",
        "\\toprule",
        "服务器 & 总聊天数 \\\\",
        "\\midrule",
    ]

    for rank in rankings:
        server_name = escape_latex(rank["server_name"])
        content.append(f"{server_name} & {rank['messages']:,} \\\\")

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/server_chat_ranking.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
