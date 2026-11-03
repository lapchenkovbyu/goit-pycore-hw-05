"""Task 3: command line log analyzer.

Usage: python main.py path/to/logfile.log [level]
"""

import sys


def parse_log_line(line: str) -> dict:
    """Parse 'DATE TIME LEVEL message' into a dict.

    Raises ValueError if the line has fewer than four parts.
    """
    parts = line.strip().split(" ", maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"malformed log line: {line.strip()!r}")
    date, time, level, message = parts
    return {"date": date, "time": time, "level": level.upper(), "message": message}


def load_logs(file_path: str) -> list:
    """Read a log file and return a list of parsed records.

    Malformed lines are skipped with a warning on stderr.
    Raises FileNotFoundError / OSError if the file cannot be read.
    """
    logs = []
    with open(file_path, "r", encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError as error:
                print(f"Warning: line {number} skipped, {error}", file=sys.stderr)
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """Return only the records whose level equals `level` (case-insensitive)."""
    return list(filter(lambda log: log["level"] == level.upper(), logs))


def count_logs_by_level(logs: list) -> dict:
    """Return {level: count}, in order of first appearance."""
    counts: dict = {}
    for log in logs:
        counts[log["level"]] = counts.get(log["level"], 0) + 1
    return counts


def display_log_counts(counts: dict) -> None:
    """Print the counts as a two column table."""
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<16} | {count}")


def main() -> None:
    """Parse arguments, load the log file and print the results."""
    if len(sys.argv) < 2:
        print("Usage: python main.py path/to/logfile.log [level]")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        sys.exit(1)
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error: cannot read '{file_path}': {error}")
        sys.exit(1)

    display_log_counts(count_logs_by_level(logs))

    if len(sys.argv) > 2:
        level = sys.argv[2].upper()
        print(f"\nДеталі логів для рівня '{level}':")
        for log in filter_logs_by_level(logs, level):
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()
