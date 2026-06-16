# plan-implement-skill

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套关于如何执行计划的方法论

## 计划执行

1. 根据 `skill-index.md` 中 “是否必须调用” 为 “是” 的列表，确保 `rules-skill.md` 已加载。
2. 若任务涉及编程，按需加载 `python-program-skill.md`（可选）。
3. 具体执行步骤按照 `plan-design-skill.md` 生成的 `PLAN-XXX.md` 中的子任务顺序进行。