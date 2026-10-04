"""Download the official CFPB Consumer Complaint Database bulk file."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import urllib.request
from pathlib import Path

try:
    from .config import SOURCE_FILE, SOURCE_URL
except ImportError:  # Direct script execution
    from config import SOURCE_FILE, SOURCE_URL


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(destination: Path = SOURCE_FILE, force: bool = False) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        print(f"Using existing file: {destination}")
        return destination

    temporary = destination.with_suffix(destination.suffix + ".part")
    print(f"Downloading {SOURCE_URL}")
    with urllib.request.urlopen(SOURCE_URL) as response, temporary.open("wb") as output:
        shutil.copyfileobj(response, output)
    temporary.replace(destination)
    print(f"Saved {destination} ({destination.stat().st_size:,} bytes)")
    print(f"SHA-256: {sha256(destination)}")
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Replace an existing raw file")
    args = parser.parse_args()
    download(force=args.force)
