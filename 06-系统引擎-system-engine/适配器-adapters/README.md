# 适配器 adapters

这里放公开版 adapter 协议和通用实现。adapter 可以知道平台公开端点、安装方法和输出格式, 但不能带走你的登录态和真实账号数据。

## 已配置

| 目录 | 用途 |
|---|---|
| `trend-sources/` | 微博、知乎、AI HOT、TrendRadar MCP 等热点来源说明 |
| `script-extraction/whisper/` | 基于 Whisper 的脚本提取流程 |
| `perf-data/douyin-session/` | 抖音创作者数据回收 adapter |
| `perf-data/xhs-explore/` | 小红书笔记数据回收 adapter |
| `perf-data/bilibili-stat/` | B 站公开视频统计 adapter |
| `perf-data/linkedin-session/` | LinkedIn 单帖分析 adapter |

## 凭据规则

1. 不提交 cookie、session、token、`.auth*/` 或 `.cheat-secrets.json`。
2. 不把真实账号数据、真实评论、真实导出和调试截图写入公开仓库。
3. 输出结构化数据, 供私有项目复盘使用。
4. 配置缺失或登录态过期时优雅失败, 降级到手动粘贴。
