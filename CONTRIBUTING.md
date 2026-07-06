# Contributing

Thanks for helping improve Chuo's Content OS.

This project has one non-negotiable contribution rule: examples must be fictional.

## Privacy checklist

Before opening a pull request, confirm that your change does not include:

- Real drafts, scripts, posts, articles, transcripts, or screenshots
- Real account names, URLs, handles, comments, or platform data
- Real benchmark accounts or competitor intelligence
- Real performance numbers from a private project
- Real rubric weights derived from private calibration
- API keys, cookies, sessions, `.env`, or databases

If a realistic example is needed, invent one and mark it as fake.

## Development

The CLI is intentionally dependency-free.

```bash
python tools/content_os.py --help
python tools/content_os.py scan-public .
```

Prefer small, plain Markdown templates over heavy automation. The system should stay inspectable by creators who do not write code.

