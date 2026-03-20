# /// script
# requires-python = ">=3.11"
# dependencies = ["resend>=2.0.0"]
# ///
"""Send emails via the Resend API."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

import resend


def check_config() -> None:
    """Verify RESEND_API_KEY is set and valid, without printing the key."""
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        print("RESEND_API_KEY: not set", file=sys.stderr)
        print("Sign up at https://resend.com and get a key from https://resend.com/api-keys", file=sys.stderr)
        sys.exit(1)

    # Validate key against the Resend API (list API keys endpoint)
    req = urllib.request.Request(
        "https://api.resend.com/api-keys",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            count = len(data.get("data", []))
            print(f"RESEND_API_KEY: valid ({count} API key(s) on account)")
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            print("RESEND_API_KEY: set but INVALID (API rejected it)", file=sys.stderr)
            print("Check your key at https://resend.com/api-keys", file=sys.stderr)
            sys.exit(1)
        # Other HTTP errors (rate limit, server error) — key format is likely fine
        print(f"RESEND_API_KEY: set (could not validate — HTTP {e.code})", file=sys.stderr)
    except Exception as e:
        print(f"RESEND_API_KEY: set (could not validate — {e})", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Send an email via the Resend API")
    parser.add_argument("--to", nargs="+", help="Recipient email address(es)")
    parser.add_argument("--subject", help="Email subject line")
    parser.add_argument("--body", help="Email body (plain text)")
    parser.add_argument("--html", help="Email body (HTML, overrides --body)")
    parser.add_argument(
        "--from",
        dest="from_addr",
        default="onboarding@resend.dev",
        help="Sender email (default: onboarding@resend.dev)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that RESEND_API_KEY is configured and valid, then exit",
    )
    args = parser.parse_args()

    if args.check:
        check_config()
        sys.exit(0)

    if not args.to or not args.subject or not args.body:
        parser.error("--to, --subject, and --body are required (unless using --check)")

    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        print("Error: RESEND_API_KEY environment variable is not set.", file=sys.stderr)
        print("Run with --check for setup instructions.", file=sys.stderr)
        sys.exit(1)

    resend.api_key = api_key

    params = {
        "from": args.from_addr,
        "to": args.to,
        "subject": args.subject,
    }
    if args.html:
        params["html"] = args.html
    else:
        params["text"] = args.body

    try:
        email = resend.Emails.send(params)
        print(f"Email sent successfully! ID: {email['id']}")
    except Exception as e:
        print(f"Failed to send email: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
