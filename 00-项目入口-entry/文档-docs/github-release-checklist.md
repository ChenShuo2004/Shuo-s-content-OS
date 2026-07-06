# GitHub 发布检查清单

发布前必须完成。

## 1. 自动扫描

```bash
python "06-系统引擎-system-engine/工具-tools/content_os.py" scan-public .
```

如果有警告，先处理，不要硬推。

## 2. 看 Git 状态

```bash
git status --short
git diff --cached
```

确认没有：

- `.env`
- cookie / token / session
- 数据库
- 截图
- 导出文件
- 真实发布稿
- 真实复盘数据
- 真实账号名
- 真实平台链接

## 3. 搜自己的敏感词

用你私有项目里的真实名称搜一遍：

```bash
rg -n "真实项目名|真实账号名|真实域名|真实产品名" .
```

工具不知道你的私有词，必须人工搜。

## 4. 检查样例

`04-创作流水线-creation-pipeline/样本-samples/` 只能放虚构样例。

允许：

- `example.com`
- fake-channel
- 虚构数据

不允许：

- 真实链接
- 真实账号
- 真实截图
- 真实评论

## 5. 先 private，后 public

先把 GitHub 仓库建成 private。

检查网页上看到的内容没有泄露，再切 public。

如果任何敏感内容进入 Git 历史，重新建干净仓库，不要直接切公开。

