import matplotlib.pyplot as plt

from stats import get_hourly_playtime, get_weekday_playtime


def create_weekday_figure(dfs, figures_dir):
    """Create weekday playtime visualization"""
    plt.rcParams["font.size"] = 16

    weekday_data = get_weekday_playtime(dfs)
    plt.figure(figsize=(15, 8))  # Increased height for better visibility

    days = [d["weekday"] for d in weekday_data]
    hours = [d["play_hours"] for d in weekday_data]

    day_names = {
        "Monday": "周一",
        "Tuesday": "周二",
        "Wednesday": "周三",
        "Thursday": "周四",
        "Friday": "周五",
        "Saturday": "周六",
        "Sunday": "周日",
    }
    x_labels = [day_names[day] for day in days]

    plt.plot(x_labels, hours, "b-o", linewidth=3, markersize=10)

    for i, hour in enumerate(hours):
        plt.text(
            i,
            hour + max(hours) * 0.05,
            f"{hour:.1f}",
            ha="center",
            va="bottom",
            fontsize=16,
        )

    plt.grid(True, linestyle="--", alpha=0.7)
    plt.title("周一到周日游玩统计", pad=20, fontsize=20)
    plt.ylabel("游玩时长（小时）", fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.tight_layout()
    plt.savefig(
        f"{figures_dir}/weekday_playtime.pdf", bbox_inches="tight", format="pdf"
    )
    plt.close()


def create_hourly_figure(dfs, figures_dir):
    """Create hourly playtime visualization"""
    plt.rcParams["font.size"] = 16

    hourly_data = get_hourly_playtime(dfs)
    plt.figure(figsize=(15, 8))  # Increased height for better visibility

    hours_x = [d["hour"].split(":")[0] for d in hourly_data]
    hours_y = [d["play_hours"] for d in hourly_data]

    plt.plot(hours_x, hours_y, "r-o", linewidth=3, markersize=10)

    for i, hour in enumerate(hours_y):
        plt.text(
            i,
            hour + max(hours_y) * 0.05,
            f"{hour:.1f}",
            ha="center",
            va="bottom",
            fontsize=16,
        )

    plt.grid(True, linestyle="--", alpha=0.7)
    plt.title("每小时游玩统计", pad=20, fontsize=20)
    plt.xlabel("小时", fontsize=18)
    plt.ylabel("游玩时长（小时）", fontsize=18)
    plt.xticks(range(0, 24, 2), fontsize=16)
    plt.yticks(fontsize=16)

    plt.tight_layout()
    plt.savefig(f"{figures_dir}/hourly_playtime.pdf", bbox_inches="tight", format="pdf")
    plt.close()


def write_frames(frames_dir):
    """Write both time distribution frames"""
    # Write weekday frame
    with open(f"{frames_dir}/weekday_distribution.tex", "w", encoding="utf-8") as f:
        f.write("""\\begin{frame}{周一到周日游玩统计}
\\begin{center}
\\includegraphics[width=\\textwidth]{figures/weekday_playtime.pdf}
\\end{center}
\\end{frame}
""")

    # Write hourly frame
    with open(f"{frames_dir}/hourly_distribution.tex", "w", encoding="utf-8") as f:
        f.write("""\\begin{frame}{每小时游玩统计}
\\begin{center}
\\includegraphics[width=\\textwidth]{figures/hourly_playtime.pdf}
\\end{center}
\\end{frame}
""")
