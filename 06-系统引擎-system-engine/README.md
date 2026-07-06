# 06 系统引擎

这一层放工具、模板、schema 和共享规范。

## 子目录

| 目录 | 用途 |
|---|---|
| `工具-tools/` | CLI 和辅助脚本 |
| `模板-templates/` | 初始化和预测使用的模板 |
| `共享规范-shared-references/` | schema、协议、数据契约 |
| `技能-skills/` | Agent skill 说明占位 |
| `钩子-hooks/` | Git/Agent hooks 占位 |
| `适配器-adapters/` | 平台数据适配器占位 |
| `迁移记录-migrations/` | 状态文件迁移说明占位 |

## 当前工具

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" --help
```

公开版工具只做文件和状态管理，不内置任何私有评分参数。

