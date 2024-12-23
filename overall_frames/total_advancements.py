from stats import get_total_advancements

def write_frame(dfs, frames_dir):
    """Generate the total advancements frame"""
    total_advs = get_total_advancements(dfs)
    
    content = [
        "\\begin{frame}{玩家总成就获得数}",
        "\\begin{center}",
        "\\vspace{2em}",
        "{\\Huge",
        f"{total_advs['total_advancements']:,} 个",  # Use comma as thousand separator
        "}",
        "\\end{center}",
        "\\end{frame}"
    ]
    
    with open(f"{frames_dir}/total_advancements.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
