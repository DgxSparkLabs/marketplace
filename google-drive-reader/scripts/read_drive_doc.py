# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-auth-oauthlib>=1.0.0",
#     "google-auth-httplib2>=0.2.0",
#     "google-api-python-client>=2.100.0",
#     "beautifulsoup4>=4.12.0",
# ]
# ///

"""Read Google Docs from personal Google Drive and extract URLs and conclusions."""

import argparse
import json
import os
import re
import sys
import uuid
from pathlib import Path
from urllib.parse import unquote

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
AUTH_DIR = Path.home() / ".auth"
DEFAULT_CREDENTIALS_FILE = AUTH_DIR / "google-drive-credentials.json"
DEFAULT_TOKEN_FILE = AUTH_DIR / "google-drive-token.json"
OUTPUT_DIR = Path("/tmp/gdrive-reader")


def _unique_output_path(extension: str = ".txt") -> Path:
    """Generate a unique output file path using a UUID4 prefix."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR / f"{uuid.uuid4().hex[:12]}{extension}"


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def _run_manual_auth_flow(credentials_file: str) -> object:
    """OAuth flow that works on headless / remote machines.

    Uses ``http://localhost`` as the redirect URI (no port-specific server
    needed).  After the user authorises, Google redirects to
    ``http://localhost?code=...``.  The browser will show a connection error
    — that's expected.  The user copies the full URL from the address bar
    and pastes it back here so we can exchange the code for tokens.
    """
    from google_auth_oauthlib.flow import InstalledAppFlow

    # Allow http://localhost redirect (safe for local OAuth loopback)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_file, SCOPES, redirect_uri="http://localhost"
    )
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

    print("\nOpen this URL in any browser and authorize access:\n")
    print(f"  {auth_url}\n")
    print("After authorizing, your browser will redirect to a localhost URL.")
    print("The page may show an error — that is expected.")
    print("Copy the FULL URL from your browser's address bar and paste it below.\n")
    redirect_url = input("Paste redirect URL: ").strip()
    flow.fetch_token(authorization_response=redirect_url)
    return flow.credentials


def get_credentials(credentials_file: str) -> object:
    """Get valid OAuth2 credentials, refreshing or running consent flow as needed."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    token_path = Path(
        os.environ.get("GOOGLE_DRIVE_TOKEN_FILE", str(DEFAULT_TOKEN_FILE))
    )
    creds = None

    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            cred_path = Path(credentials_file)
            if not cred_path.exists():
                print(f"Error: Credentials file not found: {credentials_file}", file=sys.stderr)
                print(
                    "Download OAuth2 client credentials JSON from Google Cloud Console\n"
                    "and set GOOGLE_DRIVE_CREDENTIALS_FILE to its path,\n"
                    "or run the setup wizard: bash google-drive-reader/setup.sh",
                    file=sys.stderr,
                )
                sys.exit(1)
            creds = _run_manual_auth_flow(str(cred_path))

        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json())

    return creds


# ---------------------------------------------------------------------------
# Google Drive helpers
# ---------------------------------------------------------------------------

def build_service(credentials_file: str):
    """Build and return a Drive v3 API service."""
    from googleapiclient.discovery import build

    creds = get_credentials(credentials_file)
    return build("drive", "v3", credentials=creds)


def extract_doc_id(doc_ref: str) -> str:
    """Extract a Google Doc ID from a URL, or return the input as-is."""
    patterns = [
        r"docs\.google\.com/document/d/([a-zA-Z0-9_-]+)",
        r"drive\.google\.com/file/d/([a-zA-Z0-9_-]+)",
        r"drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, doc_ref)
        if match:
            return match.group(1)
    return doc_ref.strip()


def list_docs(service, query: str | None = None, max_results: int = 20) -> list[dict]:
    """List Google Docs in the user's Drive."""
    q = "mimeType='application/vnd.google-apps.document'"
    if query:
        q += f" and fullText contains '{query}'"
    result = (
        service.files()
        .list(
            q=q,
            pageSize=max_results,
            fields="files(id, name, modifiedTime, webViewLink)",
            orderBy="modifiedTime desc",
        )
        .execute()
    )
    return result.get("files", [])


def get_doc_metadata(service, doc_id: str) -> dict:
    """Get basic metadata for a document."""
    return (
        service.files()
        .get(fileId=doc_id, fields="id,name,modifiedTime,webViewLink")
        .execute()
    )


def export_doc(service, doc_id: str, mime: str) -> str:
    """Export a Google Doc in the requested MIME type and return as string."""
    data = service.files().export(fileId=doc_id, mimeType=mime).execute()
    return data.decode("utf-8") if isinstance(data, bytes) else data


# ---------------------------------------------------------------------------
# Extraction logic
# ---------------------------------------------------------------------------

def extract_urls(html: str, self_doc_id: str = "") -> list[dict]:
    """Return a de-duplicated list of external URLs found in the document HTML."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    urls: list[dict] = []
    seen: set[str] = set()

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        text = anchor.get_text(strip=True)

        # Unwrap Google redirect wrappers
        redirect = re.search(r"google\.com/url\?q=([^&]+)", href)
        if redirect:
            href = unquote(redirect.group(1))

        # Skip fragment-only (internal bookmark) links
        if href.startswith("#"):
            continue
        # Keep only http(s) links
        if not href.startswith(("http://", "https://")):
            continue
        # Skip links that point back to this same document
        if self_doc_id and self_doc_id in href and "docs.google.com" in href:
            continue

        if href not in seen:
            seen.add(href)
            urls.append({"url": href, "text": text or "(no anchor text)"})

    return urls


def _strip_heading_number(text: str) -> str:
    """Remove leading numbering like '6.', '6.1', 'VI.', 'Chapter 6:'."""
    return re.sub(
        r"^(?:chapter\s+)?\d+[\.\):]?\s*|^[IVXLC]+[\.\)]\s*",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()


_CONCLUSION_PATTERNS = [
    r"conclusions?\s*$",
    r"summary\s+and\s+conclusions?\s*$",
    r"conclusions?\s+and\s+recommendations?\s*$",
    r"final\s+thoughts?\s*$",
    r"closing\s+remarks?\s*$",
    r"summary\s*$",
    r"key\s+takeaways?\s*$",
]


def _matches_conclusion(text: str) -> bool:
    """Return True if *text* looks like a conclusion heading."""
    stripped = _strip_heading_number(text)
    return any(re.match(p, stripped, re.IGNORECASE) for p in _CONCLUSION_PATTERNS)


def _looks_like_heading(el) -> bool:
    """Heuristic: a <p> that contains only bold / large-font text is a heading.

    Google Docs often exports headings as <p><span style="font-weight:700;
    font-size:16pt">…</span></p> instead of proper <h> tags.
    """
    if el.name != "p":
        return False
    text = el.get_text(strip=True)
    if not text or len(text) > 200:
        return False
    style = " ".join(
        span.get("style", "") for span in el.find_all("span", style=True)
    )
    has_bold = "font-weight:700" in style or "font-weight: 700" in style
    has_large = False
    size_match = re.search(r"font-size:\s*(\d+)", style)
    if size_match and int(size_match.group(1)) >= 14:
        has_large = True
    return has_bold or has_large


def extract_conclusions(html: str) -> str | None:
    """Extract a conclusion-like section from the document HTML.

    Strategy:
    1. Look for real <h1>–<h6> tags whose text matches conclusion patterns.
    2. If none found, fall back to styled <p> elements that look like headings
       (bold / large font) — common in Google Docs exports.
    3. Collect paragraph text after the match until the next heading-like element.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")

    # --- Strategy 1: proper <h> tags ---
    heading_tags = soup.find_all(re.compile(r"^h[1-6]$"))
    target = None
    for heading in heading_tags:
        if _matches_conclusion(heading.get_text(strip=True)):
            target = heading
            break

    if target is not None:
        level = target.name
        parts: list[str] = []
        for sibling in target.find_next_siblings():
            if sibling.name and re.match(r"^h[1-6]$", sibling.name):
                if sibling.name <= level:
                    break
            text = sibling.get_text(strip=True)
            if text:
                parts.append(text)
        return "\n\n".join(parts) if parts else None

    # --- Strategy 2: styled <p> headings (Google Docs fallback) ---
    #
    # Google Docs sometimes merges the heading text and body text into a
    # single <p>.  For example:
    #   <p><span style="font-weight:700">6. Conclusion</span> Body text…</p>
    #
    # We detect this by looking for a bold <span> whose text matches a
    # conclusion pattern, then collect the rest of that <p> (after the
    # heading span) plus subsequent sibling <p> elements.

    for para in soup.find_all("p"):
        for span in para.find_all("span", style=True):
            span_text = span.get_text(strip=True)
            if not span_text:
                continue
            style = span.get("style", "")
            is_bold = "font-weight:700" in style or "font-weight: 700" in style
            if is_bold and _matches_conclusion(span_text):
                target = para
                break
        if target is not None:
            break

    if target is None:
        # Strategy 3: fall back to matching the full <p> text (heading is the
        # entire paragraph, visually styled).
        for para in soup.find_all("p"):
            text = para.get_text(strip=True)
            if _matches_conclusion(text) and _looks_like_heading(para):
                target = para
                break

    if target is None:
        return None

    # The conclusion body may start inside the same <p> as the heading span.
    # Extract text from *after* the bold heading span within the same <p>.
    inline_text = ""
    heading_span = target.find("span", style=re.compile(r"font-weight:\s*700"))
    if heading_span and _matches_conclusion(heading_span.get_text(strip=True)):
        # Collect text from all siblings after the heading span within this <p>
        remaining = []
        for node in heading_span.next_siblings:
            t = node.get_text(strip=True) if hasattr(node, "get_text") else str(node).strip()
            if t:
                remaining.append(t)
        inline_text = " ".join(remaining)

    parts = []
    if inline_text:
        parts.append(inline_text)

    for sibling in target.find_next_siblings():
        if sibling.name == "p" and _looks_like_heading(sibling):
            sib_text = sibling.get_text(strip=True)
            if sib_text and len(sib_text) < 200:
                break
        text = sibling.get_text(strip=True)
        if text:
            parts.append(text)

    return "\n\n".join(parts) if parts else None


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def print_list(docs: list[dict], as_json: bool) -> None:
    if as_json:
        print(json.dumps(docs, indent=2))
        return
    if not docs:
        print("No Google Docs found.")
        return
    print(f"Found {len(docs)} document(s):\n")
    for doc in docs:
        print(f"  {doc['name']}")
        print(f"    ID:       {doc['id']}")
        print(f"    Modified: {doc.get('modifiedTime', 'unknown')}")
        print(f"    Link:     {doc.get('webViewLink', 'N/A')}")
        print()


def print_doc(
    metadata: dict,
    urls: list[dict],
    conclusions: str | None,
    full_text: str | None,
    *,
    urls_only: bool,
    conclusions_only: bool,
    as_json: bool,
) -> None:
    if as_json:
        out: dict = {
            "document": {
                "id": metadata.get("id"),
                "title": metadata.get("name"),
                "modified": metadata.get("modifiedTime"),
                "link": metadata.get("webViewLink"),
            },
        }
        if urls_only:
            out["references"] = urls
        elif conclusions_only:
            out["conclusions"] = conclusions
        else:
            out["references"] = urls
            out["conclusions"] = conclusions
            if full_text is not None:
                out["full_text"] = full_text
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    # Plain-text output
    if not urls_only and not conclusions_only:
        print(f"Document: {metadata.get('name')}")
        print(f"ID:       {metadata.get('id')}")
        print(f"Modified: {metadata.get('modifiedTime', 'unknown')}")
        print(f"Link:     {metadata.get('webViewLink', 'N/A')}")
        print()

    if not conclusions_only:
        print(f"## References ({len(urls)} URLs found)\n")
        if urls:
            for i, u in enumerate(urls, 1):
                print(f"  {i}. {u['text']}")
                print(f"     {u['url']}")
        else:
            print("  No external URLs found in this document.")
        print()

    if not urls_only:
        print("## Conclusions\n")
        if conclusions:
            print(conclusions)
        else:
            print("  No explicit conclusion section found in this document.")
        print()

    if full_text is not None and not urls_only and not conclusions_only:
        print("## Full Text\n")
        print(full_text)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read Google Docs and extract reference URLs and conclusions.",
    )
    parser.add_argument("document", nargs="?", help="Google Doc ID or URL")
    parser.add_argument("--auth", action="store_true", help="Run OAuth flow only")
    parser.add_argument("--list", action="store_true", dest="list_docs", help="List Google Docs in Drive")
    parser.add_argument("--query", "-q", help="Search query (used with --list)")
    parser.add_argument("--max-results", type=int, default=20, help="Max results for --list (default: 20)")
    parser.add_argument("--urls-only", action="store_true", help="Output only extracted URLs")
    parser.add_argument("--conclusions-only", action="store_true", help="Output only conclusions")
    parser.add_argument("--full-text", action="store_true", help="Include full document text")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    parser.add_argument(
        "--output", "-o",
        nargs="?",
        const="auto",
        default=None,
        metavar="FILE",
        help="Save output to a file instead of stdout. "
             "If no path given, auto-generates a unique filename in /tmp/gdrive-reader/",
    )
    parser.add_argument(
        "--credentials",
        default=os.environ.get(
            "GOOGLE_DRIVE_CREDENTIALS_FILE",
            os.environ.get("GOOGLE_CREDENTIALS_FILE", str(DEFAULT_CREDENTIALS_FILE)),
        ),
        help="Path to OAuth2 client credentials JSON "
             "(or set GOOGLE_DRIVE_CREDENTIALS_FILE / GOOGLE_CREDENTIALS_FILE)",
    )
    args = parser.parse_args()

    if not args.credentials or not Path(args.credentials).exists():
        print(
            "Error: Credentials file not found.\n"
            "Set GOOGLE_DRIVE_CREDENTIALS_FILE env var, pass --credentials,\n"
            "or run the setup wizard: bash google-drive-reader/setup.sh",
            file=sys.stderr,
        )
        sys.exit(1)

    # --auth: run consent flow and exit
    if args.auth:
        get_credentials(args.credentials)
        token_path = os.environ.get("GOOGLE_DRIVE_TOKEN_FILE", str(DEFAULT_TOKEN_FILE))
        print("Authentication successful. Token saved to", token_path)
        return

    if not args.list_docs and not args.document:
        parser.print_help()
        sys.exit(1)

    # --output: redirect stdout to a uniquely-named file
    output_path = None
    output_fh = None
    original_stdout = sys.stdout
    if args.output is not None:
        ext = ".json" if args.as_json else ".txt"
        if args.output == "auto":
            output_path = _unique_output_path(ext)
        else:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        output_fh = open(output_path, "w", encoding="utf-8")
        sys.stdout = output_fh

    try:
        service = build_service(args.credentials)

        # --list mode
        if args.list_docs:
            docs = list_docs(service, query=args.query, max_results=args.max_results)
            print_list(docs, as_json=args.as_json)
            return

        # Read a specific document
        doc_id = extract_doc_id(args.document)
        metadata = get_doc_metadata(service, doc_id)
        html = export_doc(service, doc_id, "text/html")

        urls = extract_urls(html, self_doc_id=doc_id)
        conclusions = extract_conclusions(html)
        full_text = export_doc(service, doc_id, "text/plain") if args.full_text else None

        print_doc(
            metadata,
            urls,
            conclusions,
            full_text,
            urls_only=args.urls_only,
            conclusions_only=args.conclusions_only,
            as_json=args.as_json,
        )
    finally:
        if output_fh is not None:
            output_fh.close()
            sys.stdout = original_stdout
            print(str(output_path))


if __name__ == "__main__":
    main()
