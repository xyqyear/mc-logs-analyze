from stats import get_death_ranking
from .common import escape_latex

def write_frame(dfs, frames_dir):
    """Generate the death ranking frame"""
    rankings = get_death_ranking(dfs)
    top_players = rankings[:10]  # Show top 10
    
    content = [
        "\\begin{frame}{死亡排行}",
        "\\begin{center}",
        "\\begin{tabular}{lr}",
        "\\toprule",
        "玩家 & 死亡次数 \\\\",
        "\\midrule"
    ]
    
    # Add each player's data
    for rank in top_players:
        player_name = escape_latex(rank['player_name'])
        content.append(f"{player_name} & {rank['deaths']:,} \\\\")
    
    content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{center}",
        "\\end{frame}"
    ])
    
    with open(f"{frames_dir}/death_ranking.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
