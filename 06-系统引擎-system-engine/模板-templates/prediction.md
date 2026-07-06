# {{TITLE}} - 预测日志

**Content ID**: `{{CONTENT_ID}}`
**Rubric Version**: `{{RUBRIC_VERSION}}`
**预测时间**: `{{PREDICTED_AT}}`
**Script Path**: `{{SCRIPT_PATH}}`
**Script Hash**: `{{SCRIPT_HASH}}`
**预测状态**: blind
**校准样本数**: `{{CALIBRATION_SAMPLES}}`
**置信度**: `{{CONFIDENCE}}`

---

## 输入快照

**Scores**: {{SCORES}}

**草稿摘要**:

{{DRAFT_SUMMARY}}

---

## Prediction

> 这是正式盲预测段。写完后不要在看到数据后回头修改，只能在 `## Retro` 里追加复盘。

**Bucket**: `{{BUCKET}}`
**Predicted Center**: `{{PREDICTED_CENTER}}`
**预测理由**: {{REASON}}

### 概率分布

| 区间 | 概率 |
|---|---:|
| 低于预期 | {{P_LOWER}} |
| 落在主预测区间 | {{P_EXPECTED}} |
| 高于预期 | {{P_HIGHER}} |

### 推理因素

| 因素 | 方向 | 置信度 | 说明 |
|---|---|---|---|
| Hook 开头张力 | TBD | TBD | TBD |
| Clarity 清晰度 | TBD | TBD | TBD |
| Specificity 具体度 | TBD | TBD | TBD |
| Resonance 共鸣 | TBD | TBD | TBD |
| Distribution 分发性 | TBD | TBD | TBD |

### 反事实

- 如果高于预测：[说明哪个判断被验证]
- 如果接近预测中心：[说明哪个基准成立]
- 如果低于预测：[说明哪个判断被推翻]

### 本次校准赌注

[把这篇内容当成一次实验，写清楚你到底在赌什么]

---

## Publish

Pending.

---

## Retro

Pending.

