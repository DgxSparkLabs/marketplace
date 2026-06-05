---
status: live
purpose: Markdown authoring conventions for this Obsidian-vault repo — link formats, headings, numbering
audience: anyone (human or agent) editing .md files here
---

# Vault Rules — Markdown authoring conventions

This repo is read **primarily in Obsidian**, secondarily on GitHub. Obsidian and GitHub resolve
in-document heading links by **different** algorithms and **no single syntax jumps in both**. We author
**Obsidian-first**: links jump in Obsidian; on GitHub they still render as links but do not navigate
(accepted trade-off). These rules exist because the TEST_YOURSELF.md table of contents cost three
debugging rounds — follow them and intra-doc links work on the first try.

## TL;DR

- **Heading links:** `[Display text](#Literal Heading Text)` — the fragment is the heading's *literal text*, NOT a GitHub kebab-slug.
- **Encode ONLY** space → `%20`, `(` → `%28`, `)` → `%29`. Leave everything else **literal**.
- **Never put a colon `:` in a heading.** Obsidian parses it as a URL scheme and the link dies. Use ` — ` (em-dash) instead of `: `.
- **Number with numbers only** (`1`, `1.1`, `1.1.1`) — no `A`/`B`/`C` letter prefixes.
- Don't put `: | [ ] ^ #` in headings.

## Rule 1 — Heading-anchor links: literal text, minimal encoding

Obsidian matches the link fragment against the heading's **literal text** (after the `#`s), then URL-decodes it.
GitHub instead *transforms* the heading into a kebab-slug. They are irreconcilable; we target Obsidian.

- ✅ **Do:** `[3.2 Node.js 18+ (required for X / Y)](#3.2%20Node.js%2018+%20%28required%20for%20X%20/%20Y%29)`
- ❌ **Don't (GitHub slug):** `[…](#32-nodejs-18-required-for-x--y)` → Obsidian: *"Unable to find 32-nodejs-…"*.
- ❌ **Don't (over-encode):** `[…](#3.2%20Node.js%2018%2B%20…%2F%20Y)` → Obsidian's decoder does **not** round-trip `%2B`,`%2F`,`%3A`,`%E2%80%94`, so the literal `+`,`/`,`:`,`—` in the heading no longer match. *Less* encoding, not more.

**Encode only what breaks Markdown link parsing.** A literal space ends the destination; a literal `)` closes the `](…)`. Everything else (`+ / , . — backtick` …) is valid in a URL fragment AND matches the heading verbatim, so leave it alone.

```python
def obsidian_fragment(heading_text_without_hashes: str) -> str:
    # encode ONLY space and parens; leave every other char literal
    return heading_text_without_hashes.replace("(", "%28").replace(")", "%29").replace(" ", "%20")
```

## Rule 2 — Forbidden characters in headings

These break Obsidian heading links and must not appear in a heading you intend to link to:

| Char | Problem | Do instead |
|---|---|---|
| `:` colon | **Known Obsidian bug** — parsed as a URL scheme (`scheme:path`), link silently fails even with `#` first | use ` — ` (em-dash) — e.g. `Setup option A — Docker`, not `Setup option A: Docker` |
| `#` | Obsidian's heading/subpath separator | omit |
| `\|` | Markdown table + wikilink alias separator | omit |
| `[` `]` | link syntax | omit |
| `^` | Obsidian block-reference marker | omit |

**Safe in headings (resolve fine):** letters, digits, spaces, `.` `-` `+` `/` `,` `—` (em-dash), and backtick `` ` `` code spans.

## Rule 3 — Section numbering: numbers only

- Number every section/subsection/test with **digits only**, hierarchical: `N` (part) → `N.M` (subsection) → `N.M.K` (one item).
- **No letter prefixes** (`A.`, `B.`…). Number front matter and appendices in the same sequence as everything else.
- Track progress by the deepest number finished (e.g. "done through **4.8.6**").

## Why Obsidian ≠ GitHub (the mechanism)

- **GitHub** generates an `id` by *transforming* heading text: lowercase → drop punctuation → spaces-to-hyphens (`## Set Up: A` → `#set-up-a`). The anchor no longer resembles the text.
- **Obsidian** does *not* transform; the anchor **is** the heading text, just URL-encoded, matched literally.

So a GitHub slug looks nothing like what Obsidian searches for, and vice-versa. This is a deliberate "which renderer jumps" choice, not a bug you can encode around. (Open Obsidian feature request to support GFM slugs has been unimplemented for years.)

## Rule 4 — When (re)generating a TOC by script

- **Be fenced-code-aware.** Lines like `# 1. Install` or `## Heading` *inside* ```` ``` ```` blocks are NOT Markdown headings — toggle an `in_fence` flag on every ```` ``` ```` and skip while inside, or you'll renumber bash comments and embedded examples.
- **Preserve line endings** (detect `\r\n` vs `\n`; don't silently rewrite the whole file to LF).
- **Preserve UTF-8** — em-dashes (`—`), checkmarks, emoji must survive the round-trip; write bytes as UTF-8.
- Generate the TOC fragments with the `obsidian_fragment()` encoder above so the outline and headings always agree.

## Sources

- [Obsidian Help — Internal links](https://obsidian.md/help/Linking+notes+and+files/Internal+links) (Markdown links must URL-encode the destination; spaces → `%20`)
- [Obsidian Forum — heading link compatibility (Obsidian vs GitHub)](https://forum.obsidian.md/t/heading-link-compatibility/46988)
- [Obsidian Forum — links with a colon don't work](https://forum.obsidian.md/t/links-including-a-colon-in-the-domain-path-component-do-not-work/8253)
- Incident this came from: the `docs/TEST_YOURSELF.md` table-of-contents fixes (2026-05 through 2026-06).
