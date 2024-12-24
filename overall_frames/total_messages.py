from stats import get_total_messages

def write_frame(dfs, frames_dir):
    """Generate the total messages frame"""
    total_msgs = get_total_messages(dfs)
    
    content = [
        "\\begin{frame}{玩家总发言数}",
        "\\begin{center}",
        "\\vspace{2em}",
        "{\\Huge",
        f"{total_msgs['total_messages']:,} 条",  # Use comma as thousand separator
        "}",
        "\\end{center}",
        "\\end{frame}"
    ]
    
    with open(f"{frames_dir}/total_messages.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
