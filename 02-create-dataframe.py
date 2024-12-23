import json
import os
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
from tqdm import tqdm

# Constants and patterns
TIME_PATTERN = r"^(\d{4}-\d{2}-\d{2})-\d\.log\.gz: \[[^\[]*(\d{2}:\d{2}:\d{2}).*?\]"
SERVER_DONE_PATTERN = r": Done \(\d.*help"
PLAYER_JOIN_PATTERN = r"(\S+?)\[\S+\] logged in with entity id \d+ at"
PLAYER_QUIT_PATTERN = r"(\S+?) lost connection: (.*)"
DEATH_MESSAGE_BASE = r"\]: (\S+) (.*)$"  # Updated death pattern
PLAYER_CHAT_PATTERN = r": (\[Not Secure\] )?<(\S+)> (.*)"

PLAYER_ADVANCEMENT_PATTERN = r"(\S+) has made the advancement \[(.*)\]"
PLAYER_ADVANCEMENT_PATTERN_ALT = r"(\S+) has just earned the achievement \[(.*)\]"

# Add exclude patterns
EXCLUDE_PATTERNS = [
    r"made the advancement",
    r"has reached",
    r"joined the game",
    r"lost connection",
    r"moved too quickly",
    r"has completed",
    r"has just earned",
    r"moved wrongly",
    r"issued server command",
    r"was kicked",
    r"is now sleeping",
    r"forced -?\d+",
    r"\(\d+",
    r"is now AFK",
    r"is no longer AFK",
]
EXCLUDE_PATTERN = "|".join(EXCLUDE_PATTERNS)

# Replace UUID extraction patterns with proper ones
PLAYER_UUID_MAPPING_PATTERN = (
    r"UUID of player (\S+) is (\S{8}-\S{4}-\S{4}-\S{4}-\S{12})"
)
PLAYER_UUID_MAPPING_PATTERN_ALT = (
    r"config to (\S+) \((\S{8}-\S{4}-\S{4}-\S{4}-\S{12})\)"
)

PLAYER_KILLED_BY_PATTERN = r"was slain by (\S+)"


def parse_timestamp(timestr: str) -> float:
    """Convert datetime string to Unix timestamp"""
    if "+" in timestr:
        dt = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S %z")
    else:
        dt = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
        # Use Asia/Shanghai timezone
        dt = dt.replace(tzinfo=ZoneInfo("Asia/Shanghai"))
    return dt.timestamp()


def timestamp_to_year(ts: float) -> int:
    """Convert Unix timestamp to year"""
    return datetime.fromtimestamp(ts, tz=ZoneInfo("Asia/Shanghai")).year


def process_advancement_files(server: str) -> list[tuple] | None:
    """Returns a list of (server, uuid, adv_name, timestamp) tuples, or None if directory doesn't exist"""
    adv_dir = Path(f"files/{server}/advancements")
    if not adv_dir.exists():
        return None

    advancements = []
    adv_files = list(adv_dir.glob("*.json"))
    for adv_file in tqdm(adv_files, desc=f"Processing {server} advancements"):
        uuid = adv_file.stem
        with open(adv_file) as f:
            data: dict[str, dict] = json.load(f)

        for adv_name, details in tqdm(
            data.items(), desc=f"Processing {uuid}", leave=False
        ):
            # Skip DataVersion, non-completed advancements, and recipe advancements
            if (
                adv_name == "DataVersion"
                or not details.get("done", False)
                or ":recipes/" in adv_name
            ):
                continue

            times = [parse_timestamp(t) for t in details["criteria"].values()]
            complete_time = max(times)
            if timestamp_to_year(complete_time) == 2024:
                advancements.append((server, uuid, adv_name, complete_time))

    return advancements


def get_uuid(player: str, uuids: dict[str, str]) -> str:
    """Get UUID for player, with warning if not found"""
    return uuids.get(player, player)


def process_server_logs(
    server: str, need_advancements: bool
) -> tuple[list, list, list, list, float | None, list, list]:  # Updated return type
    """Returns lists of sessions, deaths, messages, server info, earliest_timestamp, advancements, and name mappings"""
    log_path = Path(f"files/{server}/filtered_logs.txt")
    if not log_path.exists():
        return [], [], [], [], None, [], []

    sessions = []
    deaths = []
    messages = []
    advancements = []
    current_sessions: dict[str, float] = {}
    player_uuids: dict[str, str] = {}
    earliest_timestamp: float | None = None
    name_mappings = []  # Track (uuid, name, timestamp) tuples

    # First pass - collect UUID mappings
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if uuid_match := re.search(PLAYER_UUID_MAPPING_PATTERN, line):
                player, uuid = uuid_match.groups()
                player_uuids[player] = uuid
            elif uuid_match_alt := re.search(PLAYER_UUID_MAPPING_PATTERN_ALT, line):
                player, uuid = uuid_match_alt.groups()
                player_uuids[player] = uuid

            # Add timestamp tracking for player names
            time_match = re.search(TIME_PATTERN, line)
            if time_match and (uuid_match or uuid_match_alt):
                date_str, time_str = time_match.groups()
                timestamp = parse_timestamp(f"{date_str} {time_str}")
                # Safe access to match groups
                if uuid_match:
                    player = uuid_match.group(1)
                elif uuid_match_alt:
                    player = uuid_match_alt.group(1)
                else:
                    assert False, "Should not reach here"
                uuid = player_uuids[player]
                name_mappings.append((uuid, player, timestamp))

    def close_sessions(timestamp: float) -> None:
        for player, join_time in current_sessions.items():
            play_time = timestamp - join_time
            sessions.append(
                (
                    server,
                    get_uuid(player, player_uuids),
                    join_time,
                    play_time,
                )
            )
        current_sessions.clear()

    # Main processing pass
    total_lines = sum(1 for _ in open(log_path, "r", encoding="utf-8"))
    with open(log_path, "r", encoding="utf-8") as f:
        for line in tqdm(f, total=total_lines, desc=f"Processing {server} logs"):
            time_match = re.search(TIME_PATTERN, line)
            if not time_match:
                continue

            date_str, time_str = time_match.groups()
            timestamp: float = parse_timestamp(f"{date_str} {time_str}")

            if earliest_timestamp is None or timestamp < earliest_timestamp:
                earliest_timestamp = timestamp

            if re.search(SERVER_DONE_PATTERN, line):
                close_sessions(timestamp)
                continue

            # Process joins/quits/chat first
            if join_match := re.search(PLAYER_JOIN_PATTERN, line):
                player = join_match.group(1)
                current_sessions[player] = timestamp

            elif quit_match := re.search(PLAYER_QUIT_PATTERN, line):
                player = quit_match.group(1)
                if player in current_sessions:
                    join_time = current_sessions.pop(player)
                    sessions.append(
                        (
                            server,
                            get_uuid(player, player_uuids),
                            join_time,
                            timestamp - join_time,
                        )
                    )

            elif msg_match := re.search(PLAYER_CHAT_PATTERN, line):
                player = msg_match.group(2)
                messages.append(
                    (
                        server,
                        get_uuid(player, player_uuids),
                        msg_match.group(3),
                        timestamp,
                    )
                )

            # Process advancements before deaths, but only if needed
            elif need_advancements and (
                adv_match := re.search(PLAYER_ADVANCEMENT_PATTERN, line)
            ):
                player, adv_name = adv_match.groups()
                if player in current_sessions:
                    advancements.append(
                        (server, get_uuid(player, player_uuids), adv_name, timestamp)
                    )
            elif need_advancements and (
                adv_match := re.search(PLAYER_ADVANCEMENT_PATTERN_ALT, line)
            ):
                player, adv_name = adv_match.groups()
                if player in current_sessions:
                    advancements.append(
                        (server, get_uuid(player, player_uuids), adv_name, timestamp)
                    )

            # Process deaths last
            elif death_match := re.search(DEATH_MESSAGE_BASE, line):
                player, message = death_match.groups()
                if player in current_sessions and not re.search(
                    EXCLUDE_PATTERN, message
                ):
                    killer_uuid = None
                    if killer_match := re.search(PLAYER_KILLED_BY_PATTERN, message):
                        killer_name = killer_match.group(1)
                        killer_uuid = get_uuid(killer_name, player_uuids)

                    deaths.append(
                        (
                            server,
                            get_uuid(player, player_uuids),
                            killer_uuid if killer_uuid else message,
                            timestamp,
                        )
                    )

    close_sessions(timestamp)
    return (
        sessions,
        deaths,
        messages,
        [(server, earliest_timestamp)],
        earliest_timestamp,
        advancements,
        name_mappings,  # Add name mappings to return value
    )


def main() -> None:
    servers = [
        d for d in os.listdir("files") if os.path.isdir(os.path.join("files", d))
    ]

    all_sessions = []
    all_deaths = []
    all_messages = []
    all_advancements = []
    all_servers = []
    all_name_mappings = []

    for server in servers:
        print(f"Processing {server}")
        # Check if we need log-based advancements
        file_advancements = process_advancement_files(server)
        need_advancements = file_advancements is None

        # Process logs
        sessions, deaths, messages, servers, _, log_advancements, name_mappings = (
            process_server_logs(server, need_advancements)
        )

        # Use file-based advancements if available, otherwise use log-based
        if file_advancements is not None:
            all_advancements.extend(file_advancements)
        else:
            all_advancements.extend(log_advancements)

        all_sessions.extend(sessions)
        all_deaths.extend(deaths)
        all_messages.extend(messages)
        all_servers.extend(servers)
        all_name_mappings.extend(name_mappings)

    # Convert to DataFrames at the end
    Path("data").mkdir(exist_ok=True)

    # Create player names DataFrame with latest names
    names_df = pd.DataFrame(
        all_name_mappings, columns=["uuid", "player_name", "timestamp"]
    )
    latest_names = (
        names_df.sort_values("timestamp")
        .groupby("uuid")
        .last()
        .reset_index()[["uuid", "player_name"]]
    )
    latest_names.to_csv("data/player_names.csv", index=False)

    pd.DataFrame(all_servers, columns=["server_name", "created_timestamp"]).to_csv(
        "data/servers.csv", index=False
    )
    pd.DataFrame(
        all_sessions, columns=["server_name", "uuid", "join_timestamp", "play_time"]
    ).to_csv("data/sessions.csv", index=False)
    pd.DataFrame(all_deaths, columns=["server_name", "uuid", "by", "timestamp"]).to_csv(
        "data/deaths.csv", index=False
    )
    pd.DataFrame(
        all_messages, columns=["server_name", "uuid", "content", "timestamp"]
    ).to_csv("data/messages.csv", index=False)
    pd.DataFrame(
        all_advancements,
        columns=["server_name", "uuid", "advancement_name", "timestamp"],
    ).to_csv("data/advancements.csv", index=False)


if __name__ == "__main__":
    main()
