from stats import get_server_player_list

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the server players frame across three slides"""
    # Get server player data
    server_data = get_server_player_list(dfs)

    # Split servers into three parts
    first_group = server_data[:1]  # First server only
    remaining = server_data[1:]
    mid_point = (len(remaining) + 1) // 2  # Ensure even split of remaining servers
    second_group = remaining[:mid_point]
    third_group = remaining[mid_point:]

    # Write first slide (First server)
    if first_group:
        server = first_group[0]
        content = [
            f"\\begin{{frame}}{{{server['server_name']} 服务器玩家列表}}",
            "\\begin{center}",
            f"{server['server_name']}共有 {server['player_count']} 位玩家上线至少一次\\\\[1em]",
            "\\begin{tiny}",
            ", ".join(escape_latex(name) for name in sorted(server["player_list"])),
            "\\end{tiny}",
            "\\end{center}",
            "\\end{frame}",
        ]

        with open(f"{frames_dir}/server_players_1.tex", "w", encoding="utf-8") as f:
            f.write("\n".join(content))

    # Write second slide (First half of remaining servers)
    content = ["\\begin{frame}{服务器玩家列表 - 其他服务器 (1/2)}", "\\begin{itemize}"]

    for server in second_group:
        content.extend(
            [
                f"\\item {server['server_name']}: {server['player_count']} 位玩家",
                "\\begin{tiny}",
                f"{', '.join(escape_latex(name) for name in sorted(server['player_list']))}",
                "\\end{tiny}",
                "",
            ]
        )

    content.extend(["\\end{itemize}", "\\end{frame}"])
    with open(f"{frames_dir}/server_players_2.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    # Write third slide (Second half of remaining servers)
    content = ["\\begin{frame}{服务器玩家列表 - 其他服务器 (2/2)}", "\\begin{itemize}"]

    for server in third_group:
        content.extend(
            [
                f"\\item {server['server_name']}: {server['player_count']} 位玩家",
                "\\begin{tiny}",
                f"{', '.join(escape_latex(name) for name in sorted(server['player_list']))}",
                "\\end{tiny}",
                "",
            ]
        )

    content.extend(["\\end{itemize}", "\\end{frame}"])
    with open(f"{frames_dir}/server_players_3.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
