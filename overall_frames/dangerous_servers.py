from stats import get_dangerous_server_ranking

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the dangerous servers frame"""
    rankings = get_dangerous_server_ranking(dfs)

    content = [
        "\\begin{frame}{最危险服务器}",
        "\\small{（总死亡次数除以玩家总游玩时间）}",
        "\\begin{center}",
        "\\begin{tabular}{lrrr}",
        "\\toprule",
        "服务器 & 每小时死亡次数 & 总死亡次数 & 总游玩时长(小时) \\\\",
        "\\midrule",
    ]

    # Add each server's data
    for rank in rankings:
        server_name = escape_latex(rank["server_name"])
        content.append(
            f"{server_name} & {rank['deaths_per_hour']:.1f} & "
            f"{rank['total_deaths']:,} & {rank['play_hours']:.1f} \\\\"
        )

    content.extend(["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"])

    with open(f"{frames_dir}/dangerous_servers.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
