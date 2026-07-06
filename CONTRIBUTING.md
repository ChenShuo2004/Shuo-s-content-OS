# Contributing / 贡献说明

感谢你改进这套内容 OS。

本项目最重要的规则：**只能提交结构、模板、工具和虚构示例，不能提交真实内容资产。**

## 隐私检查

提交前确认没有包含：

- 真实草稿、文章、帖子、逐字稿
- 真实账号名、URL、评论、截图
- 真实播放量、阅读量、点赞、转发、转化数据
- 真实对标账号或竞品情报
- 真实 audience / benchmark / persona
- 私有 rubric 权重和长期复盘结论
- API key、cookie、session、`.env`、数据库

如果需要示例，请虚构，并明确标注为 fake / 虚构。

## 开发检查

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" --help
python "06-系统引擎-system-engine/工具-tools/content_os.py" scan-public .
```

CLI 尽量保持无依赖，方便非工程用户直接使用。

