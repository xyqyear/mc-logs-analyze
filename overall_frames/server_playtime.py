from stats import get_server_playtime_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the server playtime ranking frame"""
    rankings = get_server_playtime_ranking(dfs)

    content = [
        "\\begin{frame}{每个服务器总游玩时长排名}",
        "\\begin{center}",
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "服务器 & 游玩时长(小时) & 游玩时长(天) \\\\",
        "\\midrule",
    ]

    # Add each server's data
    for rank in rankings:
        server_name = escape_latex(rank["server_name"])
        content.append(
            f"{server_name} & {rank['play_hours']:,.1f} & {rank['play_days']:,.1f} \\\\"
        )

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/server_playtime.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
