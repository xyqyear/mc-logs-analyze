from stats import get_peak_concurrent_players

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Write the peak players frame"""
    with open(f"{frames_dir}/peak_players.tex", "w", encoding="utf-8") as f:
        content = [
            "\\begin{frame}{同时在线人数峰值}",
            "\\begin{center}",
            "\\begin{tabular}{lcc}",
            "\\toprule",
            "服务器 & 峰值人数 & 时刻 \\\\",
            "\\midrule",
        ]

        # Get data and sort by peak player count
        peak_data = get_peak_concurrent_players(dfs)
        peak_data.sort(key=lambda x: x["peak_players"], reverse=True)

        # Add each server's data
        for data in peak_data:
            server_name = escape_latex(data["server_name"])
            peak_time = data["peak_time"]
            content.append(f"{server_name} & {data['peak_players']} & {peak_time} \\\\")

        content.extend(
            ["\\bottomrule", "\\end{tabular}", "\\end{center}", "\\end{frame}"]
        )

        f.write("\n".join(content))
