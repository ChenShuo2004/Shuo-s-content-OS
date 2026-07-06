# 系统引擎配置说明

这个目录已经按公开版边界接入原项目的系统引擎能力。公开的是 workflow、协议、模板、hook、adapter 和通用工具, 不公开你的真实内容、账号、数据、复盘样本、对标素材和私有经验参数。

## 已接入

| 目录 | 当前内容 |
|---|---|
| `共享规范-shared-references/` | 盲预测、复盘、状态、候选池、迁移、节奏和 rubric 升级协议 |
| `钩子-hooks/` | 预测不可变、session start 和元日志 hook 配置 |
| `技能-skills/` | `cheat-*` agent skill 协议, 用于 init、打分、预测、发布、复盘、迁移、推荐等流程 |
| `模板-templates/` | workflow、status、prediction、retro、candidate、benchmark、audience、SQLite schema 和 gitignore 模板 |
| `迁移记录-migrations/` | state schema 从 1.0 到 1.4 的迁移说明 |
| `适配器-adapters/` | 热点源、语音转写、抖音/小红书/B 站/LinkedIn 数据回收 adapter |
| `工具-tools/` | 公开版 CLI、diff 百分比工具和预测曲线工具 |

## 故意不接入

- 真实测试结果、真实平台回包和调试样例。
- 历史归档里的旧文档、旧截图、旧品牌素材。
- 面向具体账号或产品的图片、主页、品牌资产生成脚本。
- 任何 `.env`、cookie、session、token、数据库、调试截图、平台导出文件。

## 路径兼容

原系统引擎的 skill 文档使用短路径:

| 上游短路径 | 公开版实际目录 |
|---|---|
| `scripts/` | `04-创作流水线-creation-pipeline/草稿-scripts/` |
| `predictions/` | `05-校准与复盘-calibration-retro/评分预测系统-scoring-prediction/预测日志-predictions/` |
| `retros/` | `05-校准与复盘-calibration-retro/复盘记录-retros/` |
| `videos/` | `04-创作流水线-creation-pipeline/已拍视频-videos/` |

`工具-tools/content_os.py` 会接受 `scripts/<file>`、`predictions/<file>`、`retros/<file>` 这些短路径别名, 对外保持轻量, 对内落到公开版编号目录。

## 凭据边界

adapter 需要登录态时, 凭据只允许存在于使用者自己的私有内容项目里, 例如 `.auth/`、`.auth-xhs/`、`.auth-linkedin/`、`.cheat-secrets.json`。这些路径已经在模板 gitignore 中屏蔽, 不应进入本公开仓库。

开源前固定运行:

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" scan-public . \
  --term <private-name-or-brand> \
  --term <private-domain-or-account>
```
