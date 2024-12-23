from stats import get_server_player_list

from .common import escape_latex


def write_frame(dfs, frames_dir):
    """Generate the server players frame across three slides"""
    # Get server player data
    server_data = get_server_player_list(dfs)

    # Separate vanilla and other servers
    vanilla_data = next(
        (s for s in server_data if s["server_name"].lower() == "vanilla"), None
    )
    other_servers = [s for s in server_data if s["server_name"].lower() != "vanilla"]

    # Find ATM9 index to split the list
    atm9_idx = next(
        (i for i, s in enumerate(other_servers) if "atm9" in s["server_name"].lower()),
        len(other_servers),
    )
    first_group = other_servers[: atm9_idx + 1]  # Include ATM9
    second_group = other_servers[atm9_idx + 1 :]  # Rest of the servers

    # Write first slide (Vanilla)
    if vanilla_data:
        content = [
            "\\begin{frame}{服务器玩家列表 - Vanilla}",
            "\\begin{center}",
            f"Vanilla共有 {vanilla_data['player_count']} 位玩家上线至少一次\\\\[1em]",
            "\\begin{tiny}",  # Use tiny font size
            ", ".join(
                escape_latex(name) for name in sorted(vanilla_data["player_list"])
            ),
            "\\end{tiny}",
            "\\end{center}",
            "\\end{frame}",
        ]

        with open(f"{frames_dir}/server_players_1.tex", "w", encoding="utf-8") as f:
            f.write("\n".join(content))

    # Write second slide (First group of servers including ATM9)
    content = ["\\begin{frame}{服务器玩家列表 - 其他服务器 (1/2)}", "\\begin{itemize}"]

    for server in first_group:
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

    # Write third slide (Remaining servers)
    content = ["\\begin{frame}{服务器玩家列表 - 其他服务器 (2/2)}", "\\begin{itemize}"]

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
    with open(f"{frames_dir}/server_players_3.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
