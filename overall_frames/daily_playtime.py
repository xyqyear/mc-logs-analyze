import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from stats import get_daily_playtime


def create_figure(dfs, figures_dir):
    """Create daily playtime heatmap"""
    # Get daily playtime data
    daily_data = get_daily_playtime(dfs)

    # Convert to DataFrame and process dates
    df = pd.DataFrame(daily_data)
    df["date"] = pd.to_datetime(df["date"])
    df["weekday"] = df["date"].dt.weekday  # 0 = Monday, 6 = Sunday
    df["week_num"] = df["date"].dt.isocalendar().week

    # Create matrix for heatmap (week x weekday)
    num_weeks = 52  # Standard number of weeks in a year
    heatmap_data = np.zeros((num_weeks, 7))  # weeks x weekdays
    week_totals = np.zeros((num_weeks, 7))

    # Calculate month boundaries for x-axis labels
    month_boundaries = []
    current_month = None

    for _, row in df.sort_values("date").iterrows():
        week_idx = int(row["week_num"]) - 1
        weekday_idx = row["weekday"]
        month = row["date"].month

        # Track month changes for labels
        if current_month != month:
            month_boundaries.append((week_idx, month))
            current_month = month

        heatmap_data[week_idx, weekday_idx] += row["play_hours"]
        week_totals[week_idx, weekday_idx] += 1

    # Calculate averages
    heatmap_data = np.divide(
        heatmap_data,
        week_totals,
        where=week_totals != 0,
        out=np.zeros_like(heatmap_data),
    )

    # Create figure
    plt.figure(figsize=(15, 4))
    plt.rcParams.update({"font.size": 16})  # Increase base font size

    # Create heatmap
    im = plt.imshow(heatmap_data.T, cmap="YlOrRd", aspect="auto")
    cbar = plt.colorbar(im, label="游玩时长（小时/天）")
    cbar.ax.tick_params(labelsize=16)  # Colorbar tick size

    # Configure axes with larger fonts
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    plt.yticks(range(7), weekday_names, fontsize=16)

    # Set x-axis ticks at month boundaries
    month_positions = [pos for pos, _ in month_boundaries]
    month_labels = [
        "1月",
        "2月",
        "3月",
        "4月",
        "5月",
        "6月",
        "7月",
        "8月",
        "9月",
        "10月",
        "11月",
        "12月",
    ][: len(month_boundaries)]
    plt.xticks(month_positions, month_labels, rotation=45, fontsize=16)

    plt.xlabel("月份", fontsize=18)
    plt.ylabel("星期", fontsize=18)
    plt.title("每周游玩时间热力图", pad=20, fontsize=20)

    # Add grid
    plt.grid(True, color="gray", linestyle=":", alpha=0.3)
    plt.tight_layout()

    # Save figure
    plt.savefig(f"{figures_dir}/daily_playtime.pdf", bbox_inches="tight", format="pdf")
    plt.close()


def write_frame(frames_dir):
    """Write the daily playtime frame TeX file"""
    with open(f"{frames_dir}/daily_playtime.tex", "w", encoding="utf-8") as f:
        f.write("""\\begin{frame}{每日游玩时间}
\\begin{center}
\\includegraphics[width=\\textwidth]{figures/daily_playtime.pdf}
\\end{center}
\\end{frame}
""")
