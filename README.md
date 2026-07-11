# Shuo's content OS

An open-source content operating system for creators, indie hackers, and AI-native founders.

It helps you turn content creation from scattered ideas into a repeatable workflow: product positioning, market research, content planning, publishing, blind prediction, performance review, and calibration.

> This repository is designed to publish the system structure and working method only. Real accounts, private drafts, real performance data, competitor notes, screenshots, cookies, sessions, tokens, and private judgment parameters should stay outside this public repository.

## What It Is

Shuo's content OS is not just a folder template.

It is a lightweight operating system for running a content-driven product or personal media project:

```text
00 Project Entry        Dashboard, workflow, operation guide
01 Product Core         Product definition, positioning, material boundaries
02 Market Research      Competitors, benchmarks, market judgment
03 Content & Sales      Platform templates, publishing checklist, content assets
04 Creation Pipeline    Drafts, samples, videos, published content
05 Calibration & Retro  Rubrics, blind predictions, reviews, audience learnings
06 System Engine        Tools, templates, schemas, adapters, shared protocols
99 Raw Materials        Placeholder for private raw exports and temporary files
```

The goal is simple:

Build a content system that gets smarter after every publish.

## Why This Exists

Most creators lose their learning loop.

They publish, check numbers, feel something, move on, and forget what they believed before the data arrived.

This system fixes that by forcing a clear loop:

1. Define the content idea.
2. Score it with a rubric.
3. Write a blind prediction before publishing.
4. Publish and collect real data.
5. Review the gap between prediction and reality.
6. Update the rubric only when the lesson is validated.

That turns content judgment from vague intuition into a calibrated asset.

## Quick Start

Requirements:

- Python 3.10+
- Git

Clone the repository:

```bash
git clone <your-repo-url>
cd "Shuo-s-content-OS"
```

Initialize a private content workspace outside the public repository:

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" init "../my-private-content-project"
python "06-系统引擎-system-engine/工具-tools/content_os.py" status "../my-private-content-project"
```

Create a draft:

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" new-script "../my-private-content-project" "My first content idea"
```

Write a blind prediction:

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" predict "../my-private-content-project" "scripts/<file-name>.md" \
  --bucket "1000-5000 views" \
  --center 2500 \
  --reason "The problem is clear, but distribution strength is average."
```

Register a published post:

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" publish "../my-private-content-project" "predictions/<file-name>.md" \
  --platform x \
  --url "https://example.com/fake-post"
```

Add a retrospective:

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" retro "../my-private-content-project" "predictions/<file-name>.md" \
  --views 3200 \
  --likes 88 \
  --comments 12 \
  --shares 6 \
  --notes "The title clarity was stronger than expected."
```

## Start Reading Here

- [Operation Guide](00-项目入口-entry/操作指南-OPERATION_GUIDE.md)
- [Project Structure](00-项目入口-entry/项目结构说明-STRUCTURE.md)
- [Workflow](00-项目入口-entry/WORKFLOW.md)
- [Privacy Model](00-项目入口-entry/文档-docs/privacy-model.md)
- [GitHub Release Checklist](00-项目入口-entry/文档-docs/github-release-checklist.md)

## Core Principles

### 1. Publish the structure, not the assets

The public repository should contain templates, tools, protocols, and examples.

Private content, real data, account details, platform exports, screenshots, and proprietary judgment should stay private.

### 2. Predict before looking at data

A prediction is only useful if it is written before real performance data appears.

After publishing, append retrospectives instead of rewriting the prediction.

### 3. Every publish must close the loop

Publishing is not the finish line.

The system learns only when you compare your original prediction with reality.

### 4. Rubrics are working tools

Validated observations can become rules.

Invalidated observations should be removed, downgraded, or rewritten.

## Public Safety Checklist

Before pushing to GitHub, run:

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" scan-public .
git status --short
```

Then manually confirm:

- No real account names, private platform URLs, or real comments.
- No real publishing lists, review data, screenshots, or exports.
- No `.env`, cookies, tokens, sessions, API keys, or databases.
- `04-创作流水线-creation-pipeline/样本-samples` contains fictional samples only.
- `99-原始资料-raw-materials` contains placeholders only, not real raw materials.

## Recommended Workflow

```text
Idea -> Draft -> Score -> Blind Prediction -> Publish -> Data -> Retro -> Rubric Update
```

This is the core loop. Everything else exists to make this loop easier to maintain.

## License

MIT. See [LICENSE](LICENSE).
