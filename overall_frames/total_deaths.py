from stats import get_total_deaths

def write_frame(dfs, frames_dir):
    """Generate the total deaths frame"""
    total_deaths = get_total_deaths(dfs)
    
    content = [
        "\\begin{frame}{玩家总死亡次数}",
        "\\begin{center}",
        "\\vspace{2em}",
        "{\\Huge",
        f"{total_deaths['total_deaths']:,} 次",  # Use comma as thousand separator
        "}",
        "\\end{center}",
        "\\end{frame}"
    ]
    
    with open(f"{frames_dir}/total_deaths.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
