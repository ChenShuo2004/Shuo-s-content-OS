# Chuo's Content OS / 绰的内容操作系统

一个面向内容创作者的开源工作流骨架：把产品资料、市场研究、平台运营、创作流水线、评分预测和复盘校准放进同一套可维护目录里。

> 这个仓库只公开“系统结构”和“操作方法”。真实账号、真实文稿、真实数据、真实对标、真实复盘和私有经验参数都不应该进入这个仓库。

## 这不是普通模板库

它不是一堆零散 Markdown，而是一套内容项目的操作系统：

```text
00 项目入口        看板、操作指南、工作流
01 产品本体        产品定义、卖点、素材边界
02 市场与竞品      竞品、对标、市场判断
03 内容与销售      平台账号、发布清单、复盘数据、素材库
04 创作流水线      草稿、样本、已拍/已发布内容
05 校准与复盘      rubric、盲预测、T+N 复盘、受众画像
06 系统引擎        工具、模板、schema、适配器、规范
99 原始资料        原始导出、临时资料，只留占位说明
```

你可以把它理解成：一个内容项目从“我要做什么”到“我怎么知道自己判断变准了”的完整工作台。

## 快速开始

需要 Python 3.10+。

```bash
git clone <your-repo-url>
cd "chuo's content OS"

python "06-系统引擎-system-engine/工具-tools/content_os.py" init "../我的私有内容项目"
python "06-系统引擎-system-engine/工具-tools/content_os.py" status "../我的私有内容项目"
```

创建草稿：

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" new-script "../我的私有内容项目" "第一篇内容标题"
```

写盲预测：

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" predict "../我的私有内容项目" "scripts/<文件名>.md" \
  --bucket "1000-5000 views" \
  --center 2500 \
  --reason "问题清楚，但分发势能一般"
```

登记发布：

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" publish "../我的私有内容项目" "predictions/<文件名>.md" \
  --platform x \
  --url "https://example.com/fake-post"
```

追加复盘：

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" retro "../我的私有内容项目" "predictions/<文件名>.md" \
  --views 3200 \
  --likes 88 \
  --comments 12 \
  --shares 6 \
  --notes "低估了标题的清晰度"
```

## 从哪里开始读

- [操作指南](00-项目入口-entry/操作指南-OPERATION_GUIDE.md)
- [项目结构说明](00-项目入口-entry/项目结构说明-STRUCTURE.md)
- [工作流速查](00-项目入口-entry/WORKFLOW.md)
- [隐私与开源边界](00-项目入口-entry/文档-docs/privacy-model.md)
- [GitHub 发布检查清单](00-项目入口-entry/文档-docs/github-release-checklist.md)

## 核心原则

1. **公开结构，不公开资产**
   开源的是目录、模板、工具、方法；私有的是内容、数据、账号、判断经验。

2. **先预测，再看数据**
   预测必须在真实数据出现前写完。预测段写完后只追加复盘，不回头改。

3. **每次发布都要结算**
   发布不是结束，T+N 复盘才是系统学习的地方。

4. **rubric 是工作台**
   被验证的观察进入规则，被推翻的观察删除或降级，不把历史噪音堆成神谕。

## 开源安全

推 GitHub 前先跑：

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" scan-public .
git status --short
```

再手动确认：

- 没有真实账号名、真实平台链接、真实评论
- 没有真实发布清单、复盘数据、截图、导出文件
- 没有 `.env`、cookie、token、session、数据库
- `04-创作流水线-creation-pipeline/样本-samples` 里只有虚构样例
- `99-原始资料-raw-materials` 只保留说明，不放真实原始资料

## License

MIT. See [LICENSE](LICENSE).
