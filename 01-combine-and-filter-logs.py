import gzip
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from tqdm import tqdm

# Regex patterns
SERVER_DONE_PATTERN = r": Done \(\d.*help"
TIME_PATTERN = r"^\[[^\[]*(\d{2}:\d{2}:\d{2}).*?\]"
PLAYER_UUID_MAPPING_PATTERN = (
    r"UUID of player (\S+) is (\S{8}-\S{4}-\S{4}-\S{4}-\S{12})"
)
PLAYER_UUID_MAPPING_PATTERN_ALT = (
    r"config to (\S+) \((\S{8}-\S{4}-\S{4}-\S{4}-\S{12})\)"
)

player_names: set[str] = set()


def parse_log_filename(filename: Path) -> tuple[str, int] | None:
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(\d+)\.log\.gz$", filename.name)
    if not match:
        return None
    date_str, index = match.groups()
    return (date_str, int(index))


def get_first_timestamp(file: Path) -> datetime | None:
    """Get the first timestamp from a log file"""
    encodings = ["utf-8", "latin1", "cp1252"]

    for encoding in encodings:
        try:
            with gzip.open(file, "rt", encoding=encoding) as f:
                for line in f:
                    match = re.search(TIME_PATTERN, line)
                    if match:
                        return datetime.strptime(match.group(1), "%H:%M:%S")
        except UnicodeDecodeError:
            continue
    return None


def get_log_files(server: str) -> list[Path]:
    log_dir = Path(f"files/{server}/logs")
    if not log_dir.exists():
        return []

    # Group files by date
    files_by_date = defaultdict(list)
    for file in log_dir.glob("*.log.gz"):
        parsed = parse_log_filename(file)
        if parsed:
            date_str, _ = parsed
            files_by_date[date_str].append(file)

    # Sort each day's files by their first timestamp
    sorted_files = []
    for date_files in files_by_date.values():
        # Get first timestamp for each file
        files_with_time = []
        for file in date_files:
            timestamp = get_first_timestamp(file)
            if timestamp:
                files_with_time.append((file, timestamp))

        # Sort by timestamp and add to result
        sorted_files.extend(
            file for file, _ in sorted(files_with_time, key=lambda x: x[1])
        )

    return sorted_files


def is_relevant_line(line: str) -> bool:
    # Check for new player names
    matches = re.findall(PLAYER_UUID_MAPPING_PATTERN, line)
    for match in matches:
        player_names.add(match[0])
        return True

    matches = re.findall(PLAYER_UUID_MAPPING_PATTERN_ALT, line)
    for match in matches:
        player_names.add(match[0])
        return True

    # Check if line is relevant
    if re.search(SERVER_DONE_PATTERN, line):
        return True
    return any(player in line for player in player_names)


def read_and_filter_log_file(file: Path) -> list[str]:
    encodings = ["utf-8", "latin1", "cp1252"]
    for encoding in encodings:
        try:
            with gzip.open(file, "rt", encoding=encoding) as f:
                return [
                    f"{file.name}: {line}"
                    for line in f.readlines()
                    if is_relevant_line(line)
                ]
        except UnicodeDecodeError:
            continue
    print(f"Warning: Could not read {file} with any encoding")
    return []


def process_server(server: str) -> None:
    player_names.clear()

    output_file = Path(f"files/{server}/filtered_logs.txt")
    log_files = get_log_files(server)

    total_lines = 0

    with open(output_file, "w", encoding="utf-8") as outf:
        for log_file in tqdm(log_files, desc=f"Processing {server} logs"):
            filtered_lines = read_and_filter_log_file(log_file)
            total_lines += len(filtered_lines)
            outf.writelines(filtered_lines)

    print(f"Found {len(player_names)} players in {server}: {player_names}")
    print(f"Wrote {total_lines} relevant lines for {server}")


def main() -> None:
    servers = [
        d for d in os.listdir("files") if os.path.isdir(os.path.join("files", d))
    ]
    for server in servers:
        print(f"\nProcessing server: {server}")
        process_server(server)
        print(f"Completed processing {server}")


if __name__ == "__main__":
    main()
