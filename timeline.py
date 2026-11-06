"""Merge timezone-aware incident records from CSV files into a UTC timeline."""
import argparse
import csv
from datetime import datetime, timezone
import json
import sys

FIELDS = ("timestamp", "source", "event", "details")


def merge(paths):
    events = []
    for path in paths:
        with open(path, encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, strict=True)
            if reader.fieldnames != list(FIELDS):
                raise ValueError(f"{path}: expected columns {','.join(FIELDS)}")
            for row in reader:
                try:
                    if None in row or any(row[key] is None for key in FIELDS):
                        raise ValueError("wrong number of columns")
                    if not row["source"].strip() or not row["event"].strip():
                        raise ValueError("source and event are required")
                    timestamp = row["timestamp"].strip()
                    if timestamp.endswith("Z"):
                        timestamp = timestamp[:-1] + "+00:00"
                    stamp = datetime.fromisoformat(timestamp)
                    if stamp.utcoffset() is None:
                        raise ValueError("timestamp requires a timezone")
                    stamp = stamp.astimezone(timezone.utc)
                except (ValueError, OverflowError) as error:
                    raise ValueError(f"{path}:{reader.line_num}: {error}") from error
                events.append((stamp, row))
    events.sort(key=lambda item: item[0])
    return [{**row, "timestamp": stamp.isoformat().replace("+00:00", "Z")}
            for stamp, row in events]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", help="CSV files to merge")
    args = parser.parse_args()
    try:
        print(json.dumps(merge(args.files), indent=2))
    except (OSError, ValueError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
