---
name: google-drive-reader
description: Read Google Docs from personal Drive, extract URLs and conclusions
argument-hint: "<doc-id-or-url | --list [--query search]>"
allowed-tools:
  - exec
  - read
permissions:
  allow:
    - Exec(uv run)
    - Exec(bash)
triggers:
  - user
  - model
---

# Google Drive Reader

Read Google Docs from a personal Google Drive (read-only). Extracts a reference
list of URLs and the conclusions section from documents.

## Prerequisites

- **uv** installed (`brew install uv` / `pip install uv`).
- **GOOGLE_DRIVE_CREDENTIALS_FILE** env var pointing to the OAuth2 client
  credentials JSON (default: `~/.auth/google-drive-credentials.json`).
- **GOOGLE_DRIVE_TOKEN_FILE** env var pointing to the saved OAuth token
  (default: `~/.auth/google-drive-token.json`).

## First-time setup

Run the interactive setup wizard — it walks through every step:

```
bash google-drive-reader/setup.sh
```

The wizard handles: Google Cloud project setup, Drive API enablement, OAuth
consent screen configuration, credentials download, environment variable
persistence, and authentication. If the script reports an authentication error,
instruct the user to re-run the setup wizard.

## Usage

### List documents

```
uv run google-drive-reader/scripts/read_drive_doc.py --list
uv run google-drive-reader/scripts/read_drive_doc.py --list --query "quarterly report"
```

### Read a document (extract URLs and conclusions)

```
uv run google-drive-reader/scripts/read_drive_doc.py <doc-id-or-url>
uv run google-drive-reader/scripts/read_drive_doc.py "https://docs.google.com/document/d/1abc.../edit"
```

### Options

| Flag                 | Description                                     |
|----------------------|-------------------------------------------------|
| `--auth`             | Run OAuth flow only, save token, then exit      |
| `--list`             | List Google Docs in Drive                       |
| `--query`, `-q`      | Search query when listing                       |
| `--max-results N`    | Max items when listing (default 20)             |
| `--urls-only`        | Print only the extracted reference URLs         |
| `--conclusions-only` | Print only the conclusions section              |
| `--full-text`        | Also include full document text in output       |
| `--json`             | Output as JSON                                  |
| `--output`, `-o`     | Save to file (auto-generates unique name if no path given) |
| `--credentials FILE` | Path to credentials JSON (overrides env var)    |

## Instructions

When the user asks you to read a Google Doc, follow these steps:

1. If the user provides a document URL or ID, read it directly:
   ```
   uv run google-drive-reader/scripts/read_drive_doc.py "<url-or-id>"
   ```

2. If the user asks to find a document by name, list and search first:
   ```
   uv run google-drive-reader/scripts/read_drive_doc.py --list --query "<search terms>"
   ```
   Then read the matching document by its ID.

3. For structured output (e.g. when you need to process the data), use `--json`.

4. To save output to a file with a unique name (avoids conflicts when multiple
   agents fetch concurrently), add `--output`:
   ```
   uv run google-drive-reader/scripts/read_drive_doc.py "<url-or-id>" --json --output
   ```
   The script prints the generated file path to stdout. Read that file for the
   content. You can also pass a specific path: `--output /tmp/my-file.json`.

5. Present the extracted **References** (URLs) as a numbered list showing the
   link text and URL. Present the **Conclusions** as a summary section.

6. If the script reports an authentication error, instruct the user to run the
   setup wizard: `bash google-drive-reader/setup.sh`

User arguments: $ARGUMENTS
