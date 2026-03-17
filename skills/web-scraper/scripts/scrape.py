# /// script
# requires-python = ">=3.11"
# dependencies = ["trafilatura>=2.0.0", "courlan>=1.0.0"]
# ///
"""Fetch a web page and extract its main content as clean text.

Includes special handling for Reddit pages (listing pages and post/comment
threads) since Reddit's HTML is not well suited for generic content extraction.
"""

import argparse
import json
import re
import sys
import urllib.request
from html import unescape

import trafilatura


_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
)


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------

def _fetch(url: str) -> str | None:
    """Fetch URL with a browser-like user-agent to avoid bot detection."""
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return downloaded
    except Exception:
        pass
    return _fetch_raw(url)


def _fetch_raw(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": _USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode(errors="replace")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Reddit-specific parsing
# ---------------------------------------------------------------------------

_REDDIT_PATTERN = re.compile(
    r"^https?://(?:www\.|old\.|new\.)?reddit\.com(/.*)?$"
)
_REDDIT_POST_PATTERN = re.compile(
    r"/r/\w+/comments/\w+"
)


def _is_reddit(url: str) -> bool:
    return bool(_REDDIT_PATTERN.match(url))


def _is_reddit_post(url: str) -> bool:
    return bool(_REDDIT_POST_PATTERN.search(url))


def _old_reddit_url(url: str) -> str:
    """Convert any reddit URL to old.reddit.com for parsing."""
    return re.sub(
        r"^https?://(?:www\.|new\.)?reddit\.com",
        "https://old.reddit.com",
        url,
    )


def _strip_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<[^>]+>", "", text)
    return unescape(text).strip()


def _scrape_reddit_listing(url: str) -> dict:
    """Parse a Reddit listing page (subreddit, front page, etc.)."""
    old_url = _old_reddit_url(url)
    html = _fetch_raw(old_url)
    if not html:
        return {"error": f"Failed to fetch {url}", "url": url}

    # Extract subreddit name from title
    title_match = re.search(r"<title>([^<]+)</title>", html)
    title = _strip_html(title_match.group(1)) if title_match else ""

    # Extract posts: each post is in a div.thing with data attributes
    posts = []
    for match in re.finditer(
        r'<div[^>]*class="[^"]*\bthing\b[^"]*"([^>]*)>',
        html,
    ):
        attrs = match.group(0)

        def _attr(name: str) -> str:
            m = re.search(rf'data-{name}="([^"]*)"', attrs)
            return m.group(1) if m else ""

        post_url = _attr("url")
        score = _attr("score") or "0"
        author = _attr("author")

        # Find the title link and comment count after this div
        rest = html[match.end():match.end() + 3000]
        title_match = re.search(
            r'<a[^>]*class="[^"]*title[^"]*"[^>]*>([^<]+)</a>', rest
        )
        comments_match = re.search(
            r'class="[^"]*comments[^"]*"[^>]*>(\d+)\s*comment', rest
        )
        n_comments = comments_match.group(1) if comments_match else "0"

        if title_match and post_url:
            post_title = _strip_html(title_match.group(1))
            full_url = post_url if post_url.startswith("http") else f"https://reddit.com{post_url}"
            posts.append({
                "title": post_title,
                "url": full_url,
                "score": score,
                "comments": n_comments,
                "author": author,
            })

    if not posts:
        return {"error": "No posts found on page", "url": url}

    lines = []
    for i, p in enumerate(posts, 1):
        lines.append(f"{i}. [{p['score']} pts, {p['comments']} comments] {p['title']}")
        lines.append(f"   by u/{p['author']} — {p['url']}")

    return {
        "url": url,
        "title": title,
        "author": "",
        "date": "",
        "sitename": "Reddit",
        "content": "\n".join(lines),
    }


def _scrape_reddit_post(url: str) -> dict:
    """Parse a Reddit post page with comments."""
    old_url = _old_reddit_url(url)
    html = _fetch_raw(old_url)
    if not html:
        return {"error": f"Failed to fetch {url}", "url": url}

    # Post title
    title_match = re.search(r'<a[^>]*class="[^"]*title[^"]*"[^>]*>([^<]+)</a>', html)
    title = _strip_html(title_match.group(1)) if title_match else ""

    # Post author
    author_match = re.search(
        r'<p class="tagline[^"]*"[^>]*>.*?class="author[^"]*"[^>]*>([^<]+)<', html, re.DOTALL
    )
    author = author_match.group(1) if author_match else ""

    # Self-text (post body) — look specifically inside the expando/post area,
    # not the sidebar.  The post body lives inside <div class="expando">
    selftext = ""
    expando_match = re.search(
        r'<div[^>]*class="[^"]*expando[^"]*"[^>]*>(.*?)</div>\s*<!--\s*/expando',
        html, re.DOTALL
    )
    if not expando_match:
        # Fallback: look for the entry div's usertext-body
        expando_match = re.search(
            r'<div[^>]*class="[^"]*entry[^"]*"[^>]*>(.*?)<div[^>]*class="[^"]*commentarea',
            html, re.DOTALL
        )
    if expando_match:
        body_match = re.search(
            r'<div class="[^"]*usertext-body[^"]*"[^>]*>\s*<div class="md">(.*?)</div>\s*</div>',
            expando_match.group(1), re.DOTALL
        )
        if body_match:
            selftext = _strip_html(body_match.group(1))

    # Link URL (for link posts)
    link_match = re.search(
        r'<a[^>]*class="[^"]*title[^"]*"[^>]*href="([^"]+)"', html
    )
    link_url = link_match.group(1) if link_match else ""

    # Comments
    comments = []
    for match in re.finditer(
        r'<div[^>]*class="[^"]*comment[^"]*"[^>]*data-author="([^"]*)"[^>]*>',
        html,
    ):
        comment_author = match.group(1)
        rest = html[match.end():match.end() + 5000]

        # Score
        score_match = re.search(r'title="(\d+) points?"', rest)
        score = score_match.group(1) if score_match else "?"

        # Comment body
        body_match = re.search(
            r'<div class="[^"]*usertext-body[^"]*"[^>]*>\s*<div class="md">(.*?)</div>\s*</div>',
            rest, re.DOTALL
        )
        body = _strip_html(body_match.group(1)) if body_match else ""

        if body:
            comments.append({
                "author": comment_author,
                "score": score,
                "body": body,
            })

    # Build output
    parts = []
    if selftext:
        parts.append(selftext)
    elif link_url and link_url != url:
        parts.append(f"Link: {link_url}")

    if comments:
        parts.append("")
        parts.append(f"--- Comments ({len(comments)} shown) ---")
        parts.append("")
        for c in comments:
            parts.append(f"u/{c['author']} ({c['score']} pts):")
            parts.append(c["body"])
            parts.append("")

    return {
        "url": url,
        "title": title,
        "author": author,
        "date": "",
        "sitename": "Reddit",
        "content": "\n".join(parts),
    }


# ---------------------------------------------------------------------------
# Generic scraping (trafilatura)
# ---------------------------------------------------------------------------

def scrape(url: str, *, include_links: bool = False, include_images: bool = False,
           include_tables: bool = True, with_metadata: bool = True,
           target_language: str | None = None) -> dict:
    """Download and extract the main content from a URL.

    Returns a dict with keys: url, title, author, date, content, and optionally
    description, sitename, categories, tags.
    """
    # Reddit-specific handling
    if _is_reddit(url):
        if _is_reddit_post(url):
            return _scrape_reddit_post(url)
        else:
            return _scrape_reddit_listing(url)

    downloaded = _fetch(url)
    if downloaded is None:
        return {"error": f"Failed to fetch {url}", "url": url}

    result = trafilatura.extract(
        downloaded,
        include_links=include_links,
        include_images=include_images,
        include_tables=include_tables,
        include_comments=False,
        output_format="txt",
        with_metadata=True,
        target_language=target_language,
        favor_recall=True,
    )

    if result is None:
        return {"error": "No extractable content found", "url": url}

    metadata = trafilatura.extract(
        downloaded,
        output_format="json",
        with_metadata=True,
        include_links=include_links,
        include_images=include_images,
        include_tables=include_tables,
        include_comments=False,
        target_language=target_language,
        favor_recall=True,
    )

    if metadata:
        meta = json.loads(metadata)
    else:
        meta = {}

    output = {
        "url": url,
        "title": meta.get("title", ""),
        "author": meta.get("author", ""),
        "date": meta.get("date", ""),
        "sitename": meta.get("sitename", ""),
        "content": result,
    }

    if with_metadata:
        for key in ("description", "categories", "tags"):
            val = meta.get(key, "")
            if val:
                output[key] = val

    return output


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Extract clean content from a web page"
    )
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--links", action="store_true",
                        help="Include hyperlinks in output")
    parser.add_argument("--images", action="store_true",
                        help="Include image references in output")
    parser.add_argument("--no-tables", action="store_true",
                        help="Exclude tables from output")
    parser.add_argument("--no-metadata", action="store_true",
                        help="Only return content, skip metadata fields")
    parser.add_argument("--language", type=str, default=None,
                        help="Target language (e.g. 'en', 'de')")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="Output as JSON instead of plain text")

    args = parser.parse_args()

    result = scrape(
        args.url,
        include_links=args.links,
        include_images=args.images,
        include_tables=not args.no_tables,
        with_metadata=not args.no_metadata,
        target_language=args.language,
    )

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result.get("title"):
            print(f"# {result['title']}")
            print()
        meta_parts = []
        if result.get("author"):
            meta_parts.append(f"By: {result['author']}")
        if result.get("date"):
            meta_parts.append(f"Date: {result['date']}")
        if result.get("sitename"):
            meta_parts.append(f"Source: {result['sitename']}")
        if meta_parts:
            print(" | ".join(meta_parts))
            print()
        if result.get("description"):
            print(f"> {result['description']}")
            print()
        print(result["content"])


if __name__ == "__main__":
    main()
