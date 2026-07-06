# File Structure

## Public repository

```text
chuo-content-os/
  README.md
  LICENSE
  CONTRIBUTING.md
  SECURITY.md
  .gitignore
  .env.example

  docs/
    workflow.md
    privacy-model.md
    file-structure.md
    github-release-checklist.md

  templates/
    script.md
    prediction.md
    retro.md
    state.json
    project/
      WORKFLOW.md
      STATUS.md
      rubric.md
      rubric-memo.md
      candidates.md
      audience.md
      script_patterns.md
      gitignore.template

  schemas/
    state.schema.json
    candidate.schema.json

  tools/
    content_os.py

  examples/
    fake-channel/
```

## Private content workspace

The CLI creates a private workspace like this:

```text
my-content-lab/
  .gitignore
  .content-os-state.json
  WORKFLOW.md
  STATUS.md
  rubric.md
  rubric-memo.md
  candidates.md
  audience.md
  script_patterns.md

  scripts/
  predictions/
  retros/
  videos/
  assets/
  exports/
```

## File Roles

| File | Role | Public? |
|---|---|---|
| `WORKFLOW.md` | Local quick reference | Template only |
| `STATUS.md` | Human dashboard | Template only |
| `rubric.md` | Current scoring rules | Generic only |
| `rubric-memo.md` | Evidence-backed observations | Private |
| `candidates.md` | Topic pool | Private |
| `audience.md` | Persona and audience model | Private |
| `script_patterns.md` | Writing patterns | Private |
| `scripts/` | Drafts and scripts | Private |
| `predictions/` | Immutable prediction logs | Private |
| `retros/` | Retrospective reports | Private |
| `videos/` | Published content folders | Private |
| `.content-os-state.json` | Workflow state | Private by default |

The public repository only includes templates and fake examples.

