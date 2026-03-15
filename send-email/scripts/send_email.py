# /// script
# requires-python = ">=3.11"
# dependencies = ["resend>=2.0.0"]
# ///
"""Send emails via the Resend API."""

import argparse
import os
import sys

import resend


def main():
    parser = argparse.ArgumentParser(description="Send an email via the Resend API")
    parser.add_argument("--to", required=True, nargs="+", help="Recipient email address(es)")
    parser.add_argument("--subject", required=True, help="Email subject line")
    parser.add_argument("--body", required=True, help="Email body (plain text)")
    parser.add_argument("--html", help="Email body (HTML, overrides --body)")
    parser.add_argument(
        "--from",
        dest="from_addr",
        default="onboarding@resend.dev",
        help="Sender email (default: onboarding@resend.dev)",
    )
    args = parser.parse_args()

    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        print("Error: RESEND_API_KEY environment variable is not set.", file=sys.stderr)
        print("Get your API key at https://resend.com/api-keys", file=sys.stderr)
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
