from stats import get_total_playtime


def write_frame(dfs, frames_dir):
    """Generate the total playtime frame"""
    total_play = get_total_playtime(dfs)

    content = [
        "\\begin{frame}{玩家总在线时长}",
        "\\begin{center}",
        "\\vspace{2em}",  # Add some vertical space
        "{\\Huge",  # Use huge font for emphasis
        f"{total_play['total_hours']:,.1f} 小时\\\\[0.5em]",
        f"({total_play['total_days']:,.1f} 天)",
        "}",  # Close huge font
        "\\end{center}",
        "\\end{frame}",
    ]

    with open(f"{frames_dir}/total_playtime.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
