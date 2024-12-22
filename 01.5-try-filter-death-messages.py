import re
from pathlib import Path
from typing import Iterator, Set

# Patterns
PLAYER_JOIN_PATTERN = r"\]: (\S+)\[.* logged in with entity"
PLAYER_QUIT_PATTERN = r"\]: (\S+) left the game"
DEATH_MESSAGE_BASE = r"\]: (\S+) (.*)$"

# Patterns to exclude
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


def read_filtered_logs(server: str) -> Iterator[str]:
    """Read filtered logs file for a server"""
    log_path = Path(f"files/{server}/filtered_logs.txt")
    if not log_path.exists():
        return
    with open(log_path, "r", encoding="utf-8") as f:
        yield from f


def extract_death_messages(server: str) -> list[str]:
    """Extract death messages for players who were online"""
    messages = []
    active_players: Set[str] = set()

    for line in read_filtered_logs(server):
        if join_match := re.search(PLAYER_JOIN_PATTERN, line):
            active_players.add(join_match.group(1))

        elif quit_match := re.search(PLAYER_QUIT_PATTERN, line):
            active_players.discard(quit_match.group(1))

        elif death_match := re.search(DEATH_MESSAGE_BASE, line):
            player, message = death_match.groups()
            if player in active_players and not re.search(EXCLUDE_PATTERN, message):
                messages.append(f"[{server}] {player}: {message}\n")

    return messages


def normalize_death_message(message: str) -> str:
    """Remove server and player info to get the core death message"""
    # Remove server and player prefix like "[server] playername: "
    message = re.sub(r"^\[[^\]]+\] \S+: ", "", message)
    # Remove trailing newline
    return message.strip()


def main() -> None:
    unique_output = Path("files/unique_death_messages.txt")

    servers = [
        d.name
        for d in Path("files").iterdir()
        if d.is_dir() and (d / "filtered_logs.txt").exists()
    ]

    death_counts = {}

    for server in servers:
        print(f"Processing server: {server}")
        messages = extract_death_messages(server)

        # Count unique death messages
        for msg in messages:
            normalized = normalize_death_message(msg)
            death_counts[normalized] = death_counts.get(normalized, 0) + 1

        print(f"Found {len(messages)} death messages")

    # Write unique messages with counts
    with open(unique_output, "w", encoding="utf-8") as f:
        for msg, count in sorted(death_counts.items(), key=lambda x: (-x[1], x[0])):
            f.write(f"[{count:4d}] {msg}\n")

    print(f"\nWrote {len(death_counts)} unique death messages to {unique_output}")


if __name__ == "__main__":
    main()
