from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

from stats import get_server_timeline


def create_figure(dfs, figures_dir):
    """Create the server timeline figure"""
    # Configure Chinese font support
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False

    # Get server timeline data and process
    timeline = get_server_timeline(dfs)
    for server in timeline:
        server["created_datetime"] = datetime.fromisoformat(server["created_at"])
        server["closed_datetime"] = datetime.fromisoformat(server["closed_at"])
        if server["server_name"].lower() == "vanilla":
            server["display_name"] = f"{server['server_name']} (2020-10-01)"
        elif server["server_name"].lower() == "gtnh":
            server["display_name"] = f"{server['server_name']} (???)"
        else:
            server["display_name"] = server["server_name"]

    timeline.sort(key=lambda x: x["created_datetime"])

    # Create visualization
    plt.figure(figsize=(15, 12))
    ax = plt.gca()
    colors = plt.cm.tab20(np.linspace(0, 1, len(timeline)))  # type: ignore

    # Draw timeline elements
    for idx, server in enumerate(timeline):
        y_pos = len(timeline) - idx - 1
        plt.hlines(
            y=y_pos,
            xmin=server["created_datetime"],
            xmax=server["closed_datetime"],
            linewidth=8,
            color=colors[idx],
        )

        time_diff = (
            server["closed_datetime"] - server["created_datetime"]
        ).total_seconds()
        min_time_for_both_dates = 24 * 60 * 60

        plt.text(
            server["created_datetime"],
            y_pos + 0.1,
            f"{server['display_name']}\n{server['created_datetime'].strftime('%m-%d')}",
            verticalalignment="bottom",
            fontsize=24,
            linespacing=0.8,
        )

        if time_diff >= min_time_for_both_dates:
            plt.text(
                server["closed_datetime"],
                y_pos + 0.1,
                f"{server['closed_datetime'].strftime('%m-%d')}",
                verticalalignment="bottom",
                fontsize=24,
                horizontalalignment="left",
            )

    # Configure plot
    plt.ylim(-0.3, len(timeline) - 0.3)
    plt.yticks([])
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    plt.xticks(rotation=45, fontsize=24)
    plt.grid(True, axis="x")

    # Save figure (without ensuring directory exists)
    plt.tight_layout()
    plt.savefig(f"{figures_dir}/server_timeline.pdf", bbox_inches="tight", format="pdf")
    plt.close()


def write_frame(frames_dir):
    """Write the timeline frame TeX file"""
    with open(f"{frames_dir}/timeline.tex", "w", encoding="utf-8") as f:
        f.write("""\\begin{frame}{服务器时间线}
\\begin{center}
\\includegraphics[width=\\textwidth]{figures/server_timeline.pdf}
\\end{center}
\\end{frame}
""")
