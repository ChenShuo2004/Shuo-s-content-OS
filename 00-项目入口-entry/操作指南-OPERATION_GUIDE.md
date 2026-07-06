# 操作指南

这份指南按“日常真的怎么用”写，不按技术模块写。

## 0. 准备

公开仓库只放系统骨架。你应该另建一个私有内容项目来保存真实内容：

```text
chuo-content-os/          # 公开仓库
我的私有内容项目/          # 私有仓库或本地目录
```

## 1. 初始化私有项目

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" init "../我的私有内容项目"
```

初始化后会生成同样的编号架构：

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

## 2. 填产品本体

进入私有项目的 `01-产品本体-product-core/`，先写清楚：

- 你提供什么产品/服务/知识体系
- 它解决什么问题
- 目标用户是谁
- 哪些素材可以公开讲，哪些不能讲
- 核心卖点和证据是什么

没有产品本体，后面的内容会变成散点。

## 3. 建平台工作区

在 `03-内容与销售-content-sales/` 下复制 `平台模板-platform-template`，改名成你的平台，比如：

```text
03-内容与销售-content-sales/
  X/
  小红书/
  抖音/
  公众号/
```

每个平台下保持同样结构：

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

## 4. 创建草稿

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" new-script "../我的私有内容项目" "这篇内容的标题"
```

草稿会进入：

```text
04-创作流水线-creation-pipeline/草稿-scripts/
```

你可以手动改写这个草稿。真正用于发布的最终稿，应该在预测前稳定下来。

CLI 会输出两行：真实路径和命令别名。后续命令建议用短别名，例如：

```text
scripts/2026-07-06_xxxxxxxx_title.md
```

## 5. 写盲预测

在看到任何发布数据之前运行：

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" predict "../我的私有内容项目" "<草稿路径>" \
  --bucket "1000-5000 views" \
  --center 2500 \
  --reason "一句话说明为什么这么预测"
```

预测会进入：

```text
05-校准与复盘-calibration-retro/
  评分预测系统-scoring-prediction/
    预测日志-predictions/
```

预测写完后不要改预测段。后面只能追加发布信息和复盘。

预测日志也可以用短别名：

```text
predictions/2026-07-06_xxxxxxxx_title.md
```

## 6. 发布登记

内容发布后登记 URL：

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" publish "../我的私有内容项目" "<预测日志路径>" \
  --platform x \
  --url "https://example.com/fake-post"
```

这一步会把该预测加入待复盘队列。

## 7. T+N 复盘

默认 T+3 天复盘。拿到数据后运行：

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" retro "../我的私有内容项目" "<预测日志路径>" \
  --views 3200 \
  --likes 88 \
  --comments 12 \
  --shares 6 \
  --notes "这次验证/推翻了什么"
```

复盘会同时：

- 追加到预测日志底部
- 复制一份到 `05-校准与复盘-calibration-retro/复盘记录-retros/`
- 更新 `.content-os-state.json`

## 8. 更新 rubric

不要单篇内容一失败就改规则。

建议满足这些条件再改：

- 至少 5 篇完成复盘
- 连续 3 次出现同方向偏差
- 新观察能解释多个样本
- 新规则在历史样本上更能排序

记录路径：

```text
05-校准与复盘-calibration-retro/rubric-memo.md
```

稳定后再抽象进：

```text
05-校准与复盘-calibration-retro/rubric_notes.md
```

## 9. 查看状态

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" status "../我的私有内容项目"
```

你会看到：

- 当前 rubric 版本
- 已完成复盘数量
- 待复盘队列
- 最近草稿/预测/发布/复盘

## 10. 开源前检查

在公开仓库执行：

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" scan-public .
```

再人工检查一遍。不要把私有项目直接开源。
