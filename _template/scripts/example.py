# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""REPLACE: Short description of what this script does."""

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="REPLACE: Script description")
    parser.add_argument("--flag", required=True, help="REPLACE: Flag description")
    parser.add_argument("--optional", help="REPLACE: Optional flag description")
    args = parser.parse_args()

    # Check for required environment variables
    api_key = os.environ.get("SOME_API_KEY")
    if not api_key:
        print("Error: SOME_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    # REPLACE: Implement the skill logic here
    print(f"Running with flag={args.flag}")


if __name__ == "__main__":
    main()
