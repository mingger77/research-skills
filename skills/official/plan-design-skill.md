# plan-design-skill

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套能够用于在科研中科研计划制定的方法论。

1. 创建科研计划 `workspace/docs/main/PLAN-[serial]`。
2. 在制定 `PLAN-[serial]` 时，应考虑：
   - 用户的科研目标
   - `SUMMERY.md`
   - `RESULT-[serial]`（可选）
3. `PLAN-[serial]` 应包含以下方面的内容：
   - **目标拆解**（子任务、验收标准）：
     - 子任务输入
     - 子任务输出
     - 子任务成功标准
     - 子任务失败判定条件
   - 可能遇到的困难及备选方案（至少 1 项）
   - Baseline 方案
   若计划编写Python程序，必须包含：
     - Python 依赖库列表（含版本建议）
     - 核心代码逻辑（伪代码或结构化描述）
4. 等待用户批准 `PLAN.md` 后，才能进入 **计划执行**。