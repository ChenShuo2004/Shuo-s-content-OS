# Workflow

Chuo's Content OS turns content creation into a calibration loop.

```text
Candidate -> Draft -> Score -> Blind prediction -> Publish -> Retro -> Rubric update
```

## 1. Candidate

候选项是“可能值得做”的素材，不是承诺。

来源可以是：

- 自己想到的选题
- 热点
- 用户问题
- 读书笔记
- 竞品启发
- 旧内容的延伸

候选项进入 `candidates.md`，至少包含标题和来源。打分前不要直接推荐。

## 2. Draft

草稿放在 `scripts/`。

命名建议：

```text
YYYY-MM-DD_<12-char-id>_<short-slug>.md
```

同一个内容从草稿、预测、发布到复盘都使用同一个 id。这样后续可以稳定追踪。

## 3. Score

打分是探索动作，可以重复。

推荐从 5 个通用维度开始：

| Dimension | Meaning |
|---|---|
| Hook | 开头是否快速形成问题张力 |
| Clarity | 观点是否清楚，读者是否知道你要说什么 |
| Specificity | 是否有具体场景、对象、例子 |
| Resonance | 是否触发情绪、身份、困境或欲望 |
| Distribution | 是否天然容易被转发、引用、讨论 |

公开版只提供通用 rubric。你的真实权重应该留在私有工作区。

## 4. Blind Prediction

盲预测是正式承诺。

要求：

- 必须在看到数据之前写
- 必须写预测 bucket 和中心值
- 必须写理由
- 必须写反事实：如果高于/低于预测，说明哪个判断错了
- 写完后不修改预测段，只能追加复盘

CLI:

```bash
python tools/content_os.py predict <project> <script-path> --bucket "1k-5k views" --center 2500 --reason "..."
```

## 5. Publish

发布登记只写元数据：

- platform
- URL
- published_at
- prediction file

CLI:

```bash
python tools/content_os.py publish <project> <prediction-path> --platform x --url "https://example.com/post/123"
```

发布后，该预测进入 `pending_retros`。

## 6. Retro

复盘不是写感想，而是结算预测。

至少记录：

- views / reads
- likes
- comments
- shares
- prediction center
- actual result
- error percentage
- what was validated
- what was falsified
- what should enter `rubric-memo.md`

CLI:

```bash
python tools/content_os.py retro <project> <prediction-path> --views 3200 --likes 88 --comments 12 --shares 6 --notes "..."
```

## 7. Rubric Update

不要因为单篇内容就改规则。

推荐触发条件：

- 至少 5 篇完成复盘
- 连续 3 次同方向偏差
- 新观察能够解释多个样本
- 新规则在历史样本上更能排序

更新路径：

```text
rubric-memo.md -> 抽象 -> rubric.md -> 重新检查历史样本
```

`rubric-memo.md` 可以有证据和样本名。`rubric.md` 只能保留抽象规则，不应该含真实 URL、评论或私有数据。

