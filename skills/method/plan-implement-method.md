# plan-implement-method

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套关于如何执行科研计划的方法论。

---

## 执行前准备

1. 确认当前存在已批准的计划文档（`PLAN-XXX.md`），且 `PROJECT_META.json` 中的 `active_plan` 指向该文件。
2. 确认执行环境已就绪（如虚拟环境、依赖库等），若缺失则按相应 skill 准备。

---

## 计划执行

1. 按照 `PLAN-XXX.md` 中定义的子任务顺序依次执行。
2. 每个子任务执行前：
   - 检查该子任务的前置依赖是否已完成。
   - 向用户报告即将执行的子任务内容。
3. 子任务执行过程中：
   - 若涉及编程，加载 `python-program-method.md`。
   - 若需要临时文件，遵循 `temp-file-handle-method.md`。
   - 所有关键操作按 `log-write-constraint.md` 记录。
4. 若实验包含随机过程（如随机种子、采样、初始化等），**至少运行 3 次**，并记录每次的参数和结果。
5. 子任务完成后：
   - 根据 `rules.md` 中的停止机制，向用户报告完成情况并等待确认。
   - 更新 `PROJECT_META.json` 中的执行进度（如当前完成的子任务编号）。

---

## 执行结束

1. 所有子任务完成后，更新 `PROJECT_META.json` 中的 `current_state` 为 `EXECUTING_COMPLETE`。
2. 向用户报告：“计划执行完成，请确认是否进入结果分析阶段？ `[yes/no]`
3. 用户确认后，进入 `result-handle-method.md` 阶段。

---

## 异常处理

1. 若某个子任务连续失败 3 次（按 `rules.md` 定义），停止执行并向用户报告。
2. 若执行过程中断（如用户终止），记录当前进度到 `PROJECT_META.json`，便于后续恢复。
