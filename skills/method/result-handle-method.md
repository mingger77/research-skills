# result-handle-method

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套能够用于在科研中进行 **结果记录** 和 **结果总结** 的方法论。

## 相关 skill 加载

1. 在进行 **结果记录** 之前，必须加载 `result-write-constraint.md`
2. 在进行 **结果总结** 之前，必须加载 `report-write-constraint.md`

## 结果记录

1. 将实验结果写入文档 `workspace/docs/result/RESULT` 中
2. 参考 `log-write-constraint`，创建日志 `EXPERIMENT_LOG.md`。
。

## 结果总结

1. 当用户明确要求"总结"或"结束本轮研究"时，参考 `report-write-constraint` 生成 `workspace/docs/main/REPORT`。
2. 若 `REPORT` 能回答 `PLAN` 中的科研目标，进入 `COMPLETION` 状态
3. 当 `REPORT` 指出"无法回答科研目标"时，Agent 应：
   - 分析现有结果与原始目标的差距
   - 提出 1~2 种改进路径（如：修改参数、更换模型、重新收集数据）
   - 回退 `PLAN-DESIGNING` 状态
   - 生成 `PLAN-[serial + 1]`（例如当前 `PLAN-001.md`，则生成 `PLAN-002.md`）
4. 同一科研目标，迭代超过 3 次后，应该：
   - 停止科研任务
   - 生成 `FINAL_REPORT.md`

