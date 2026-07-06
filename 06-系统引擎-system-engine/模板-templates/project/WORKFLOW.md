# 工作流

```text
产品本体 -> 市场竞品 -> 平台策略 -> 草稿 -> 盲预测 -> 发布 -> T+N 复盘 -> 更新 rubric
```

## 日常命令

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" status .
python "06-系统引擎-system-engine/工具-tools/content_os.py" new-script . "标题"
python "06-系统引擎-system-engine/工具-tools/content_os.py" predict . "scripts/<文件名>.md" --bucket "1000-5000 views" --center 2500 --reason "..."
python "06-系统引擎-system-engine/工具-tools/content_os.py" publish . "predictions/<文件名>.md" --platform x --url "https://example.com/fake-post"
python "06-系统引擎-system-engine/工具-tools/content_os.py" retro . "predictions/<文件名>.md" --views 3200 --likes 88 --comments 12 --shares 6 --notes "..."
```

## 纪律

1. 先写预测，再看数据。
2. 预测段写完后不改。
3. 发布后必须复盘。
4. 观察先进 `rubric-memo.md`，多次验证后再进 `rubric_notes.md`。
