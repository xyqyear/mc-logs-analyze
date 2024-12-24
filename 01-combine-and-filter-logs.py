import gzip
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterator

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


def read_gzipped_file(file: Path) -> Iterator[str]:
    """Read a gzipped file with multiple encodings and yield lines

    Args:
        file: Path to gzipped file

    Yields:
        Each line from the file
    """
    encodings = ["utf-8", "latin1", "cp1252"]
    for encoding in encodings:
        try:
            with gzip.open(file, "rt", encoding=encoding) as f:
                yield from f
            return  # If we get here, we successfully read the file
        except UnicodeDecodeError:
            continue
    print(f"Warning: Could not read {file} with any encoding")


def parse_log_filename(filename: Path) -> tuple[str, int] | None:
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(\d+)\.log\.gz$", filename.name)
    if not match:
        return None
    date_str, index = match.groups()
    return (date_str, int(index))


def get_first_timestamp(file: Path) -> datetime | None:
    """Get the first timestamp from a log file"""
    for line in read_gzipped_file(file):
        match = re.search(TIME_PATTERN, line)
        if match:
            try:
                return datetime.strptime(match.group(1), "%H:%M:%S")
            except ValueError:
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


def read_and_filter_log_file(file: Path) -> Iterator[str]:
    """Read and filter log lines, yielding only relevant ones"""
    return (
        f"{file.name}: {line}"
        for line in read_gzipped_file(file)
        if is_relevant_line(line)
    )


def process_server(server: str) -> None:
    player_names.clear()

    output_file = Path(f"files/{server}/filtered_logs.txt")
    log_files = get_log_files(server)

    total_lines = 0

    with open(output_file, "w", encoding="utf-8") as outf:
        for log_file in tqdm(log_files, desc=f"Processing {server} logs"):
            for line in read_and_filter_log_file(log_file):
                outf.write(line)
                total_lines += 1

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
