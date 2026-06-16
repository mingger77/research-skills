# result-handle-skill

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套能够用于在科研中进行 **结果记录** 和 **结果总结** 的方法论。

## 结果记录

1. 将实验结果写入文档 `workspace/docs/result/RESULT-[serial]` 中
2. `RESULT-[serial]` 至少包含：
   - 每次运行前自动记录所用参数（包括随机种子）
   - 是否成功运行（exit code）
   - 核心结果（数值、图片、表格）所在位置
3. 创建日志 `workspace/docs/log/EXPERIMENT_LOG.md`，日志必须包含：
   - 时间
   - Git Commit
   - 数据集版本
   如果运行了Python程序，则应包含：
     - 参数
     - 随机种子
     - Python 版本
     - 依赖版本

## 结果总结

1. 当用户明确要求"总结"或"结束本轮研究"时，生成 `workspace/main/REPORT-[serial]`。
2. `REPORT-[serial]` 至少包含：
   - 结果是否与 `PLAN-[serial]` 中的目标一致
   - 若一致：用 1~2 句话总结结论
   - 若不一致：
     - 列出至少 2 条可能原因
     - 提出至少 1 条修改建议
   - 当前结果是否能回答 `PLAN.md` 中的科研目标
     - 若能，结束进程
     - 若不能，跳到本小节第 6 步
3. 当 `REPORT.md` 指出"无法回答科研目标"时，Agent 应：
   - 分析现有结果与原始目标的差距
   - 提出 1~2 种改进路径（如：修改参数、更换模型、重新收集数据）
   - 生成 `PLAN-[serial + 1]`
   - 停止并向用户报告："已生成新计划，是否继续？"
   - 用户批准后，重复执行 **实行步骤**（从虚拟环境或代码修改开始，可复用之前环境）

