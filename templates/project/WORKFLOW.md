# Content OS Workflow

```text
Candidate -> Draft -> Score -> Blind prediction -> Publish -> Retro -> Rubric update
```

## Daily Commands

```bash
python /path/to/content_os.py status .
python /path/to/content_os.py new-script . "Title"
python /path/to/content_os.py predict . scripts/<file>.md --bucket "1k-5k views" --center 2500 --reason "..."
python /path/to/content_os.py publish . predictions/<file>.md --platform x --url "https://example.com/post"
python /path/to/content_os.py retro . predictions/<file>.md --views 3200 --likes 88 --comments 12 --shares 6 --notes "..."
```

## Rules

1. Write prediction before data.
2. Do not edit prediction after it is written.
3. Append retro with actual data.
4. Move observations from `rubric-memo.md` into `rubric.md` only after repeated evidence.

