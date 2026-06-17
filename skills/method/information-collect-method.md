# information-collect-method

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套可用于在科研中进行 **资料查找**、 **资料分析** 和 **资料总结** 的方法论。

---

## 相关 skill 加载

1. 在进行 **原始资料处理** 之前，必须加载 `information-collect-constraint.md` 

## 原始资料处理

1. 用户提供的所有资料存放于 `workspace/docs/raw/` 中。
2. 根据用户是否提供资料及资料格式：
   - 若无资料 → 直接进入 **资料收集** 部分
   - 若资料是 Office/txt → 先转换为 markdown（规则见 `skills/temp-file-handle-method`）
   - 若资料已是 markdown → 直接使用
3. 所有处理后的 markdown 文档统一放入 `workspace/docs/processed/`。

---

## 资料收集

### 资料检索

1. 对资料进行检索

### 联网搜寻

1. 结合用户研究方向及用户提供的资料，在网上搜寻相关资料。

### 资料去重

1. 筛去重复的低价值资料，留下高质量资料

### 资料记录

1. 将搜寻的资料写入文档 `workspace/docs/processed/INFORMATION-[level]-[serial].md` 中，例如 `INFORMATION-A-01.md`。
2. 参考 `log-write-constraint`，创建日志 `SEARCH_LOG.md`。

---

## 资料分析

### 偏见控制

1. 对寻找到的资料进行偏见控制

### 资料重要性判定

1. 将 `workspace/docs/processed/` 中的所有资料从对于本课题的重要性的角度划分以下三个量级：`High` / `Medium` / `Low`。
2. 根据重要性等级，对每篇资料进行内容遴选：
   - **High**：
     - 完整摘要（研究问题、方法、主要结论、关键数据/图表描述）
     - 每篇摘要控制在 200~400 字
     - 标注 "核心参考"
   - **Medium**：
     - 精简摘要（仅研究问题和主要结论）
     - 每篇摘要控制在 80~150 字
     - 标注 "补充参考"
   - **Low**：
     - 一律一句话总结，不超过 40 字（除非用户明确要求详细）
     - 标注 "一般参考"

### 资料整合

1. 创建总结 `workspace/docs/main/SUMMARY.md`。
2. 完成后向用户报告：共处理资料 X 篇，其中 High Y 篇、Medium Z 篇、Low W 篇， `SUMMARY.md` 已生成。
