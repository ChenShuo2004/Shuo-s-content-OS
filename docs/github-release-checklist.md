# GitHub Release Checklist

Run this before making the repository public.

## 1. Scan

```bash
python tools/content_os.py scan-public .
```

Fix every high-confidence warning.

## 2. Inspect Git status

```bash
git status --short
git diff --cached
```

Look for:

- `.env`
- database files
- screenshots
- exports
- real URLs
- real usernames
- real comments
- raw materials
- private workspaces

## 3. Search for sensitive terms

Use terms from your private project:

```bash
rg -n "account-name|project-name|real-domain|api_key|token|cookie|session" .
```

Do not rely on the default scanner alone. You know your private names better than the tool does.

## 4. Verify examples

Everything under `examples/` must be fake.

Good:

```text
Quiet Builder Notes
https://example.com/fake-post
```

Bad:

```text
Real platform links
Real handles
Real screenshots
Real performance data
```

## 5. Push private first

Create the GitHub repo as private first.

```bash
git remote add origin <private-github-url>
git push -u origin main
```

Open GitHub in the browser and inspect files as a stranger would.

## 6. Switch public only after review

After review, change repository visibility from private to public in GitHub settings.

If anything sensitive entered Git history, do not switch public. Rewrite history or create a fresh clean repo.

