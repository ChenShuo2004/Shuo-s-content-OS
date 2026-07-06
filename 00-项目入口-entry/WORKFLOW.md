# 工作流速查

```text
产品本体 -> 市场竞品 -> 平台策略 -> 草稿 -> 盲预测 -> 发布 -> T+N 复盘 -> 更新 rubric
```

## 一次完整循环

1. 在 `01-产品本体-product-core/` 确认这篇内容服务哪个产品/问题。
2. 在 `02-市场与竞品-market-research/` 查对标和市场语境。
3. 在 `03-内容与销售-content-sales/<平台>/` 确认平台定位和发布位置。
4. 在 `04-创作流水线-creation-pipeline/草稿-scripts/` 写草稿。
5. 在 `05-校准与复盘-calibration-retro/` 用 rubric 打分。
6. 在数据出现前写盲预测。
7. 发布后登记 URL。
8. T+N 天后追加复盘。
9. 把新观察写入 `rubric-memo.md`。
10. 多个样本验证后再更新 `rubric_notes.md`。

## 常用命令

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" status .
python "06-系统引擎-system-engine/工具-tools/content_os.py" new-script . "标题"
python "06-系统引擎-system-engine/工具-tools/content_os.py" predict . "scripts/<文件名>.md" --bucket "1000-5000 views" --center 2500 --reason "..."
python "06-系统引擎-system-engine/工具-tools/content_os.py" publish . "predictions/<文件名>.md" --platform x --url "https://example.com/fake-post"
python "06-系统引擎-system-engine/工具-tools/content_os.py" retro . "predictions/<文件名>.md" --views 3200 --likes 88 --comments 12 --shares 6 --notes "..."
```

## 三条禁令

1. 没写预测就不要看数据。
2. 写完预测不要回头改。
3. 不要把真实数据放进公开仓库。
