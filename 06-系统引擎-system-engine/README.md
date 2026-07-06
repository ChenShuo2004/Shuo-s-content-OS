# 06 系统引擎

这一层是公开版的 workflow 运行内核: 工具、模板、schema、skill 协议、hook、adapter 和迁移记录都放在这里。

## 子目录

| 目录 | 用途 |
|---|---|
| `工具-tools/` | CLI、公开扫描、diff 和预测曲线辅助脚本 |
| `模板-templates/` | 初始化、预测、复盘、候选池、rubric、audience、SQLite schema 模板 |
| `共享规范-shared-references/` | 盲预测、状态、候选池、复盘、迁移、节奏、升级协议 |
| `技能-skills/` | `cheat-*` agent skill 协议 |
| `钩子-hooks/` | 预测不可变、session start、元日志 hook |
| `适配器-adapters/` | 热点源、脚本提取、平台表现数据 adapter |
| `迁移记录-migrations/` | state schema 迁移说明 |

## 公开版边界

已配置的是方法和程序骨架, 不是你的内容资产。真实账号、真实文稿、真实复盘数据、cookie、token、数据库、截图、平台导出和私有经验参数都不应进入仓库。

详细边界见 [配置说明-CONFIGURATION.md](配置说明-CONFIGURATION.md)。

## 当前工具

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" --help
```

开源前扫描:

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" scan-public . \
  --term <private-name-or-brand> \
  --term <private-domain-or-account>
```

说明: 内部 skill 名称暂保留 `cheat-*`, 这是为了兼容已导入的上游协议和 hook。公开仓库外层仍以 Content OS 的编号目录作为主结构。
