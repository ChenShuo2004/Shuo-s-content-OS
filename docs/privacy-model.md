# Privacy Model

这个项目的开源边界是：公开工作流，不公开内容资产。

## Public

可以公开：

- 方法论
- 空白模板
- schema
- CLI 工具
- 虚构示例
- 通用 rubric
- 文件结构说明
- 发布前检查清单

## Private

必须保留在私有工作区：

- 真实稿件、文章、帖子、视频脚本
- 真实预测日志
- 真实复盘数据
- 真实播放量、阅读量、点赞、评论、分享
- 真实平台 URL
- 真实账号名、handle、用户评论
- 对标账号、竞品拆解、商业信息
- audience/persona/benchmark
- 真实 rubric 权重和长期经验参数
- `.env`、cookie、token、session、数据库
- 截图、导出文件、原始素材

## Recommended Repo Split

```text
public repo
  docs/
  templates/
  schemas/
  tools/
  examples/fake-channel/

private repo
  scripts/
  predictions/
  retros/
  videos/
  candidates.md
  rubric.md
  rubric-memo.md
  audience.md
  benchmark.md
  .content-os-state.json
```

## Why Not Open the Existing Repo

如果一个敏感文件曾经被 commit，即使后来删除，公开 Git 历史里仍然可能看到它。

安全做法是白名单复制：

1. 新建公开目录
2. 只放确认可以公开的文件
3. 用虚构示例替代真实案例
4. 扫描敏感词和文件类型
5. 先推 private repo 检查
6. 再切 public

不要在现有私有仓库上“删掉敏感文件后开源”。

## Example Rules

可以写：

```text
Fake Channel: Quiet Builder Notes
Prediction: 1k-5k views
Actual: 3.2k views
```

不要写：

```text
真实账号名
真实发布链接
真实评论截图
真实销售转化
真实对标对象
```

## Gitignore Is Not a Security Boundary

`.gitignore` 只能防止未来误提交。它不能保护已经提交过的文件，也不能替代人工检查。

发布前必须跑：

```bash
python tools/content_os.py scan-public .
git status --short
```

然后手动检查 `git diff --cached`。

