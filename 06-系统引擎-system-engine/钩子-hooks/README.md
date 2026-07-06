# 钩子 hooks

这里放 workflow 自动化 hook。公开版已经接入:

- `prediction-immutability.sh` / `.json`: 阻止事后修改预测段。
- `session-start.sh` / `.json`: 会话开始时读取状态并提示待复盘事项。
- `log-event.sh` / `meta-logging.json`: 记录轻量本地事件元数据, 不记录原始提示词正文。

这些 hook 是可选能力。使用者应把配置复制到自己的私有内容项目中启用, 不要把 `.auth*/`、`.cheat-cache/` 或平台调试数据提交到公开仓库。
