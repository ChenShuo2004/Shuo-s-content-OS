# 操作指南

这份指南按日常使用来写: 你可以用 Codex 或 Claude 做执行和判断, 用 Obsidian 做长期阅读、编辑和检索。核心原则只有一个: 公开仓库放系统, 私有项目放真实内容。

## 1. 先分清两个目录

| 目录 | 用途 | 能不能公开 |
|---|---|---|
| `chuo‘s content OS/` | 开源系统骨架、CLI、模板、协议、adapter、操作方法 | 可以公开 |
| `我的私有内容项目/` | 真实产品、真实草稿、真实账号、真实数据、真实复盘 | 不要公开 |

推荐放法:

```text
D:/coding/chuo‘s content OS/        # 公开仓库, 也就是这个项目
D:/coding/my-content-workspace/     # 你的私有内容项目, 名字自定
```

之后所有真实内容都写进私有项目。公开仓库只负责提供工具和方法。

## 2. 第一次初始化

在公开仓库根目录运行:

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" init "D:/coding/my-content-workspace"
python "06-系统引擎-system-engine/工具-tools/content_os.py" status "D:/coding/my-content-workspace"
```

初始化后, 私有项目会生成同样的编号结构:

```text
00-项目入口-entry/
01-产品本体-product-core/
02-市场与竞品-market-research/
03-内容与销售-content-sales/
04-创作流水线-creation-pipeline/
05-校准与复盘-calibration-retro/
06-系统引擎-system-engine/
99-原始资料-raw-materials/
.content-os-state.json
```

下一步打开 Obsidian, 把 `D:/coding/my-content-workspace/` 作为 vault。不要把公开仓库当成日常内容 vault。

## 3. 三种使用方式

### Codex

适合做文件操作、批量整理、跑命令、生成草稿、写预测、检查仓库。

建议开两个工作区:

- 维护系统时打开 `D:/coding/chuo‘s content OS/`
- 日常创作时打开 `D:/coding/my-content-workspace/`

日常可以这样对 Codex 说:

```text
请读取 00-项目入口-entry/STATUS.md 和 WORKFLOW.md, 告诉我下一步该做什么。
```

```text
围绕这个选题帮我新建一篇草稿, 放到草稿目录, 并告诉我后续预测命令。
```

```text
给 scripts/<文件名>.md 写一份盲预测。注意: 不要读取任何发布后的数据。
```

```text
我已经发布了这篇, URL 是 https://example.com/fake-post, 帮我登记发布。
```

```text
这是 T+3 数据: 播放 3200, 点赞 88, 评论 12, 分享 6。帮我写复盘并更新状态。
```

### Claude

适合长对话、拆选题、改文稿、按 skill 协议走完整工作流。Claude 使用时也应该在私有内容项目里操作, 不要把真实内容写回公开仓库。

推荐提示词:

```text
你现在在我的私有内容项目中。请先读 00-项目入口-entry/操作指南-OPERATION_GUIDE.md、WORKFLOW.md、STATUS.md, 然后按 Content OS 流程协助我。
```

如果要使用系统引擎里的 skill 协议, 让 Claude 读取公开仓库里的对应文件:

```text
请按 D:/coding/chuo‘s content OS/06-系统引擎-system-engine/技能-skills/cheat-predict/SKILL.md 的协议, 为这篇稿子写盲预测。
```

```text
请按 D:/coding/chuo‘s content OS/06-系统引擎-system-engine/技能-skills/cheat-retro/SKILL.md 的协议, 处理这次复盘。
```

Claude 中最重要的约束:

- 预测必须在看到真实数据前写。
- 预测写完后不要回头改预测段。
- 真实账号、cookie、token、导出数据只放私有项目, 不放公开仓库。

### Obsidian

适合做长期知识库、手动编辑、回看复盘、维护产品资料和平台资料。

把私有项目作为 Obsidian vault 后, 建议收藏这些文件:

```text
00-项目入口-entry/STATUS.md
00-项目入口-entry/WORKFLOW.md
01-产品本体-product-core/
03-内容与销售-content-sales/
04-创作流水线-creation-pipeline/草稿-scripts/
05-校准与复盘-calibration-retro/rubric_notes.md
05-校准与复盘-calibration-retro/rubric-memo.md
05-校准与复盘-calibration-retro/评分预测系统-scoring-prediction/预测日志-predictions/
05-校准与复盘-calibration-retro/复盘记录-retros/
```

Obsidian 里适合你手动做:

- 写产品本体、卖点、边界和素材说明。
- 改草稿正文。
- 看历史预测和复盘。
- 整理对标账号、受众画像、平台策略。
- 从复盘中提炼 `rubric-memo.md`。

Obsidian 里不建议手动做:

- 手改 `.content-os-state.json`。
- 手改已经写完的预测段。
- 把平台导出、cookie、截图、真实用户评论放进公开仓库。

## 4. 每天怎么跑

### Step 1: 看状态

```bash
python "D:/coding/chuo‘s content OS/06-系统引擎-system-engine/工具-tools/content_os.py" status "D:/coding/my-content-workspace"
```

先看有没有待复盘、最近草稿、最近预测。不要一上来就写新东西。

### Step 2: 确认产品和平台

在 Obsidian 里看:

```text
01-产品本体-product-core/
03-内容与销售-content-sales/<平台>/
```

本次内容至少要回答:

- 服务哪个产品或问题。
- 发到哪个平台。
- 目标用户是谁。
- 这次内容想验证什么判断。

### Step 3: 新建草稿

```bash
python "D:/coding/chuo‘s content OS/06-系统引擎-system-engine/工具-tools/content_os.py" new-script "D:/coding/my-content-workspace" "这篇内容的标题"
```

草稿会进入:

```text
04-创作流水线-creation-pipeline/草稿-scripts/
```

CLI 会输出短路径, 例如:

```text
scripts/2026-07-06_xxxxxxxx_title.md
```

后续命令优先用这个短路径。

### Step 4: 写盲预测

在发布前、看到任何真实数据前运行:

```bash
python "D:/coding/chuo‘s content OS/06-系统引擎-system-engine/工具-tools/content_os.py" predict "D:/coding/my-content-workspace" "scripts/<文件名>.md" \
  --bucket "1000-5000 views" \
  --center 2500 \
  --reason "一句话说明为什么这样预测"
```

预测会进入:

```text
05-校准与复盘-calibration-retro/评分预测系统-scoring-prediction/预测日志-predictions/
```

写完后只允许追加发布和复盘信息, 不要修改预测判断。

### Step 5: 发布登记

发布后登记 URL:

```bash
python "D:/coding/chuo‘s content OS/06-系统引擎-system-engine/工具-tools/content_os.py" publish "D:/coding/my-content-workspace" "predictions/<文件名>.md" \
  --platform x \
  --url "https://example.com/fake-post"
```

这一步会把该预测加入待复盘队列。

### Step 6: T+N 复盘

拿到数据后运行:

```bash
python "D:/coding/chuo‘s content OS/06-系统引擎-system-engine/工具-tools/content_os.py" retro "D:/coding/my-content-workspace" "predictions/<文件名>.md" \
  --views 3200 \
  --likes 88 \
  --comments 12 \
  --shares 6 \
  --notes "这次验证或推翻了什么"
```

复盘会同时:

- 追加到预测日志底部。
- 复制一份到 `05-校准与复盘-calibration-retro/复盘记录-retros/`。
- 更新 `.content-os-state.json`。

### Step 7: 更新 rubric

不要因为单篇内容就改规则。建议先把观察写进:

```text
05-校准与复盘-calibration-retro/rubric-memo.md
```

满足这些条件后, 再沉淀到:

```text
05-校准与复盘-calibration-retro/rubric_notes.md
```

建议条件:

- 至少 5 篇完成复盘。
- 连续 3 次出现同方向偏差。
- 新观察能解释多个样本。
- 新规则能让历史样本排序更合理。

## 5. 平台资料怎么放

在私有项目里, 每个平台复制一份:

```text
03-内容与销售-content-sales/平台模板-platform-template/
```

然后改名:

```text
03-内容与销售-content-sales/
  X/
  小红书/
  抖音/
  公众号/
```

每个平台保持同样结构:

```text
00-平台总览/
01-账号定位/
02-发布清单/
03-复盘数据/
04-策略素材/
05-配图库/
06-视觉资产/
07-对标账号/
08-文章库/
```

真实账号信息、发布数据和评论都只放在私有项目中。

## 6. 开源前检查

只在公开仓库运行:

```bash
cd "D:/coding/chuo‘s content OS"
python "06-系统引擎-system-engine/工具-tools/content_os.py" scan-public . \
  --term <你的名字或品牌> \
  --term <你的账号名或域名>
git status --short
```

再人工确认:

- 没有真实账号名、真实平台链接、真实评论。
- 没有真实发布清单、复盘数据、截图、导出文件。
- 没有 `.env`、cookie、token、session、数据库。
- `99-原始资料-raw-materials/` 只保留说明, 不放真实原始资料。
- 私有内容项目没有被误复制进公开仓库。

## 7. 常见问题

### 我应该在 Codex 打开哪个目录?

改系统和开源仓库时打开 `D:/coding/chuo‘s content OS/`。日常写内容时打开 `D:/coding/my-content-workspace/`。

### Obsidian 应该打开哪个目录?

打开私有内容项目。公开仓库可以偶尔阅读, 但不要把它当日常写作 vault。

### 可以不用命令行吗?

可以。你可以让 Codex 或 Claude 代跑命令。但你要明确告诉它当前操作的是私有项目, 以及公开仓库的 CLI 路径。

### 可以直接在 Obsidian 里建草稿吗?

可以, 但建议文件放到:

```text
04-创作流水线-creation-pipeline/草稿-scripts/
```

文件名最好带日期和短标题。之后预测时把路径给 Codex 或 Claude。

### 发布后忘了预测怎么办?

不要补写“盲预测”。这篇只能做普通复盘或标记为非盲样本, 不要放进校准统计里。

### 什么时候需要回到公开仓库?

只有三种情况:

- 更新操作指南、模板、CLI 或 adapter。
- 准备开源发布。
- 把某个私有项目里验证过的通用方法抽象成模板。

## 8. 一句话流程

```text
看状态 -> 定产品/平台 -> 写草稿 -> 数据出现前写预测 -> 发布登记 -> T+N 复盘 -> 记入 rubric-memo -> 多样本验证后更新 rubric_notes
```
