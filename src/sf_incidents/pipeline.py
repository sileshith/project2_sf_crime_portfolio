from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .artifacts import build_aggregates, write_aggregates
from .constants import PROCESSED_DIR
from .data import fetch_datasf, load_local


def main() -> None:
    parser = argparse.ArgumentParser(description="Build reproducible dashboard artifacts")
    parser.add_argument("--source", type=Path, help="Local CSV/Parquet; omit to fetch DataSF")
    parser.add_argument("--output", type=Path, default=PROCESSED_DIR)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    incidents = load_local(args.source) if args.source else fetch_datasf()
    source = str(args.source) if args.source else "DataSF dataset wg3w-h783"
    metadata = write_aggregates(
        build_aggregates(incidents), args.output, source=source, source_rows=len(incidents)
    )
    print(f"Built artifacts from {metadata['source_rows']:,} canonical incident rows")


if __name__ == "__main__":
    main()
