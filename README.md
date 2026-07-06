# Chuo's Content OS

把内容创作变成一个可复盘、可校准、可进化的工作流。

这个仓库是公开版骨架，只包含方法、模板、schema 和本地小工具。它不包含任何真实账号、真实稿件、真实复盘、真实评论、真实平台数据或私有经验参数。

## 它解决什么

大多数内容创作的问题不是没有发布，而是每次发布之后没有留下可比较的判断记录。

Chuo's Content OS 把一篇内容拆成一个闭环：

```text
候选选题 -> 草稿 -> 打分 -> 盲预测 -> 发布登记 -> T+N 复盘 -> 更新 rubric
```

核心不是让 AI 替你写爆款，而是让你的判断留下账本。每一次“我觉得这篇会好”都要在数据出现前写下来，数据出现后再结算。

## 公开版包含什么

- `docs/`: 工作流说明、隐私边界、文件结构、GitHub 发布检查清单
- `templates/`: 私有内容工作区可复制的 Markdown 模板
- `schemas/`: 状态文件和候选池的 JSON Schema
- `tools/content_os.py`: 无依赖 Python CLI，用来初始化工作区、生成脚本、写预测、登记发布、追加复盘、做公开前扫描
- `examples/fake-channel/`: 完全虚构的示例频道

## 公开版不包含什么

- 真实选题池
- 真实脚本、文章、帖子、视频逐字稿
- 真实播放量、阅读量、评论、转化数据
- 真实对标账号和竞品拆解
- 真实 audience/persona/benchmark
- 真实 rubric 权重、长期复盘沉淀、失败样本
- API key、cookie、session、`.env`、数据库

如果你要把自己的内容系统开源，请只开源这个骨架。真实内容应该放在独立的私有工作区。

## 快速开始

需要 Python 3.10+。

```bash
git clone <your-repo-url>
cd "chuo's content OS"

python tools/content_os.py init ../my-private-content-lab
python tools/content_os.py status ../my-private-content-lab
```

创建第一篇草稿：

```bash
python tools/content_os.py new-script ../my-private-content-lab "Why creators need prediction logs"
```

写一份盲预测日志：

```bash
python tools/content_os.py predict ../my-private-content-lab scripts/2026-07-06_abcd1234_topic.md \
  --bucket "1k-5k views" \
  --center 2500 \
  --reason "Clear problem, narrow audience, weak distribution."
```

发布后登记：

```bash
python tools/content_os.py publish ../my-private-content-lab predictions/2026-07-06_abcd1234_topic.md \
  --platform x \
  --url "https://example.com/post/123"
```

T+N 天后复盘：

```bash
python tools/content_os.py retro ../my-private-content-lab predictions/2026-07-06_abcd1234_topic.md \
  --views 3200 \
  --likes 88 \
  --comments 12 \
  --shares 6 \
  --notes "Underestimated clarity; distribution was stronger than expected."
```

推 GitHub 前扫描公开目录：

```bash
python tools/content_os.py scan-public .
```

## 三条原则

1. 盲预测先于数据  
   预测必须在看到实际表现之前写完。预测段写完后只能追加复盘，不能回头改。

2. 复盘必须引用数据  
   不写“感觉不错”。写“预测中心 2500 views，实际 3200 views，偏高 28%”。

3. rubric 是工作台，不是博物馆  
   被数据推翻的观察要删掉或降级。被验证成规则的观察要抽象进 rubric，而不是永久堆在 memo 里。

## 推荐使用方式

公开仓库保存 workflow。私有仓库保存你的内容资产。

```text
public/chuo-content-os/
  docs/
  templates/
  schemas/
  tools/
  examples/

private/my-content-lab/
  scripts/
  predictions/
  retros/
  videos/
  rubric.md
  rubric-memo.md
  audience.md
  candidates.md
  .content-os-state.json
```

## GitHub 发布前

先运行：

```bash
python tools/content_os.py scan-public .
git status --short
```

再人工检查：

- 没有真实账号名
- 没有真实 URL
- 没有真实评论
- 没有平台截图
- 没有 `.env`、cookie、token、session
- 没有数据库或导出文件
- `examples/` 里的内容全部是虚构的

更多细节见 [docs/privacy-model.md](docs/privacy-model.md) 和 [docs/github-release-checklist.md](docs/github-release-checklist.md)。

## License

MIT. See [LICENSE](LICENSE).

