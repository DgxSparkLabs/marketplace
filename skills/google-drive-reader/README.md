# google-drive-reader

Read Google Docs from a personal Google Drive (read-only access) and extract
reference URLs and conclusions.

## What it does

Given a Google Doc URL or ID, this skill:

1. **Extracts references** — collects all external hyperlinks in the document
   into a numbered reference list with link text and URL.
2. **Extracts conclusions** — finds the conclusion/summary section of the
   document and returns its contents.

It can also list and search your Google Docs by name.

## Quick start

Run the interactive setup wizard — it walks you through every step with clear
instructions, validates your setup, and handles common pitfalls:

```bash
bash google-drive-reader/setup.sh
```

The wizard covers: Google Cloud project creation, Drive API enablement, OAuth
consent screen setup, credentials download, environment variable persistence,
authentication, and a final connection test.

If you prefer to set things up manually, follow the detailed steps below.

## Manual setup

### 1. Create a Google Cloud project and enable the Drive API

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Go to **APIs & Services > Library**.
4. Search for **Google Drive API** and click **Enable**.

> **Pitfall — "Google Drive API has not been used in project … before or it is
> disabled":** This 403 error means you skipped this step or the API hasn't
> propagated yet. After enabling, wait 1-2 minutes before retrying.

### 2. Configure the OAuth consent screen

1. Go to **APIs & Services > OAuth consent screen**.
2. Choose **External** user type (unless you have a Workspace org), click
   **Create**.
3. Fill in the required fields (app name, support email) — the name you choose
   here is what you'll see on the consent page (e.g. "agent-skill").
4. On the **Scopes** step, add the scope
   `https://www.googleapis.com/auth/drive.readonly`.
5. Complete the wizard and save.

By default the consent screen is in **Testing** mode. This means only
explicitly listed test users can authorize.

> **Pitfall — "app has not completed the Google verification process … Error
> 403: access_denied":** You need to add your own Google account as a test
> user. Go to **OAuth consent screen > Test users > Add users** and enter the
> Gmail address you will authorize with.

Alternatively, for personal-only use you can click **Publish App** on the
consent screen overview to switch from Testing to Production. Google won't
require full verification for apps with fewer than 100 users and read-only
scopes.

### 3. Create OAuth credentials

1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials > OAuth client ID**.
3. Application type: **Desktop app**. Give it any name.
4. Click **Create**.
5. Click **Download JSON** and save the file to a safe location:

```bash
mkdir -p ~/.auth
# Move or copy the downloaded file:
mv ~/Downloads/client_secret_*.json ~/.auth/google-drive-credentials.json
```

> **Pitfall — redirect URI:** Desktop-app type credentials automatically
> include `http://localhost` as an authorized redirect URI, which is what this
> script uses. If you accidentally created a "Web application" type credential
> instead, the auth flow will fail with a redirect_uri_mismatch error. Delete
> it and create a Desktop app credential.

### 4. Set environment variables

```bash
export GOOGLE_DRIVE_CREDENTIALS_FILE="$HOME/.auth/google-drive-credentials.json"
export GOOGLE_DRIVE_TOKEN_FILE="$HOME/.auth/google-drive-token.json"
```

Add these lines to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) so they
persist across sessions. Without them, the script falls back to the default
paths in `~/.auth/` but won't find credentials if they're stored elsewhere.

### 5. Authenticate (one-time)

```bash
uv run google-drive-reader/scripts/read_drive_doc.py --auth
```

The script will print an authorization URL. Open it in any browser (even on a
different machine), sign in with your Google account, and grant read-only
access. After authorizing:

1. Google redirects your browser to `http://localhost?code=...`.
2. The page will show a **"site can't be reached"** error — this is expected,
   especially on remote/headless machines.
3. Copy the **full URL** from your browser's address bar (it starts with
   `http://localhost/?state=...&code=...`).
4. Paste it back into the terminal when prompted.

On success you'll see:

```
Authentication successful. Token saved to ~/.auth/google-drive-token.json
```

The token refreshes automatically on future runs. You only need to repeat this
step if you revoke access or delete the token file.

> **Pitfall — "insecure_transport" error:** This occurred in an earlier version
> and has been fixed. The script sets `OAUTHLIB_INSECURE_TRANSPORT=1`
> internally to allow the `http://localhost` redirect, which is safe for local
> OAuth loopback flows.

## Validating the setup

Run these commands in order to confirm everything is working:

### Step 1 — Check credentials file exists

```bash
ls -la "$GOOGLE_DRIVE_CREDENTIALS_FILE"
# or if env var is not set:
ls -la ~/.auth/google-drive-credentials.json
```

Expected: the file is listed. If you get "No such file or directory", revisit
step 3 above.

### Step 2 — Check token was saved

```bash
ls -la ~/.auth/google-drive-token.json
```

Expected: the file exists. If not, re-run `--auth`.

### Step 3 — List your documents

```bash
uv run google-drive-reader/scripts/read_drive_doc.py --list
```

Expected: a numbered list of your recent Google Docs with names, IDs, and
links. If you see:
- **403 "Drive API has not been used"** — enable the API (step 1).
- **403 "access_denied"** — add yourself as a test user (step 2).
- **"No credentials file specified"** — set the env var (step 4).
- **"Credentials file not found"** — check the file path (step 3).

### Step 4 — Read a document

Pick any document ID from the listing and run:

```bash
uv run google-drive-reader/scripts/read_drive_doc.py <doc-id>
```

Expected: the document title, a list of extracted reference URLs, and a
conclusions section (or a note that no conclusions heading was found).

## Usage

### List your Google Docs

```bash
uv run google-drive-reader/scripts/read_drive_doc.py --list
uv run google-drive-reader/scripts/read_drive_doc.py --list --query "meeting notes"
```

### Read a document

```bash
# By URL
uv run google-drive-reader/scripts/read_drive_doc.py "https://docs.google.com/document/d/1aBcDe.../edit"

# By document ID
uv run google-drive-reader/scripts/read_drive_doc.py 1aBcDeFgHiJkLmNoPqRsTuVwXyZ
```

### Options

| Flag                 | Description                                  |
|----------------------|----------------------------------------------|
| `--auth`             | Run OAuth flow and save token, then exit     |
| `--list`             | List recent Google Docs                      |
| `--query`, `-q`      | Search query (with `--list`)                 |
| `--max-results N`    | Max items when listing (default 20)          |
| `--urls-only`        | Output only the extracted reference URLs     |
| `--conclusions-only` | Output only the conclusions section          |
| `--full-text`        | Include full document text in output         |
| `--json`             | Output as JSON                               |
| `--credentials FILE` | Path to credentials JSON (overrides env var) |

### Examples

```bash
# Get only URLs as JSON
uv run google-drive-reader/scripts/read_drive_doc.py "https://docs.google.com/document/d/1abc.../edit" --urls-only --json

# Get conclusions from a doc
uv run google-drive-reader/scripts/read_drive_doc.py 1aBcDe... --conclusions-only

# Full document dump with references and conclusions
uv run google-drive-reader/scripts/read_drive_doc.py 1aBcDe... --full-text
```

## As an Agent Skill

Copy the `google-drive-reader` directory into your agent's skills folder:

```bash
# Global install
cp -r google-drive-reader ~/.config/devin/skills/google-drive-reader

# Project-level install
cp -r google-drive-reader .devin/skills/google-drive-reader
```

Then invoke it with `/google-drive-reader <doc-url>` or let the agent use it
autonomously when it needs to read a Google Doc.

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_DRIVE_CREDENTIALS_FILE` | `~/.auth/google-drive-credentials.json` | Path to OAuth2 client credentials JSON |
| `GOOGLE_DRIVE_TOKEN_FILE` | `~/.auth/google-drive-token.json` | Path to saved OAuth token |
| `GOOGLE_CREDENTIALS_FILE` | _(none)_ | Legacy alias for credentials (fallback if `GOOGLE_DRIVE_CREDENTIALS_FILE` is not set) |

All authentication files are stored in `~/.auth/` by default. The setup wizard
configures these automatically.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Credentials file not found` | Env var not set or wrong path | Set `GOOGLE_DRIVE_CREDENTIALS_FILE` or place file at `~/.auth/google-drive-credentials.json` |
| `403: Google Drive API has not been used` | Drive API not enabled | Enable it in Cloud Console > APIs & Services > Library |
| `403: access_denied` | OAuth consent screen in Testing mode, your email not listed | Add your email under OAuth consent screen > Test users |
| `redirect_uri_mismatch` | Credential type is "Web application" instead of "Desktop app" | Delete and recreate as Desktop app type |
| `InsecureTransportError` | Old script version without localhost exemption | Update to latest version of the script |
| Auth URL printed but redirect fails | Remote machine, no browser redirect possible | Copy the full URL from the browser address bar after the error page loads, paste it back |
| `Token has been expired or revoked` | Token too old or access revoked in Google account | Delete `~/.auth/google-drive-token.json` and re-run `--auth` |

## Limitations

- Only reads **Google Docs** (not Sheets, Slides, PDFs, etc.).
- Conclusion extraction relies on the document having a heading named
  "Conclusion", "Summary", "Key Takeaways", or similar. Documents without an
  explicit section heading will report no conclusions found.
- Requires the one-time interactive OAuth consent flow before non-interactive
  use.
