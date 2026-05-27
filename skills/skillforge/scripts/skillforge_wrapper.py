#!/usr/bin/env python3
"""Wrapper script that delegates to the skillforge CLI."""
import subprocess
import sys


def main():
    args = sys.argv[1:]
    try:
        result = subprocess.run(["skillforge"] + args, text=True)
    except FileNotFoundError:
        result = subprocess.run([sys.executable, "-m", "src.cli.main"] + args, text=True)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
