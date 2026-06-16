# skill-index

这个索引旨在给以 Claude Code 为代表的 Agent 提供一个关于指导 Agent 进行科研活动的一系列 skill 的索引。

## 索引介绍

`skill-index.md` 清晰的列出了每一个 skill 的 **skill名称**， **类别**， **位置**， **是否必须调用** 和 **简述**

1. **skill名称**：规定了调用skill的正式名称
2. **类别**：规定了 skill 的类别
   - 类别为 **大纲** 的 skill 规定 Agent 在科研活动中怎么安排
   - 类别为 **约束** 的 skill 规定 Agent 在科研活动中怎么做
   - 类别为 **方法** 的 skill 规定 Agent 在科研活动中做什么
3. **位置**：规定了 skill 的位置
4. **是否必须调用**：规定了 skill 在科研流程中是否一定会被调用
5. **简述***：描述了 skill 的大致功能

## 正式索引

| **skill名称**| **类别**| **位置**| **是否必须调用**| **简述**|
|------|-----|------|------|
| main-skill.md | 大纲 | skills/main/main-skill.md | 是 | 科研流程的总调度器，定义步骤顺序和技能加载规则 |
| rules-skill.md | 约束 | skills/main/rules-skill.md | 是 | 用于规范Agent在科研活动中的行为 |
| information-collect-skill.md | 方法 | skills/official/information-collect-skill.md | 是 | 用于资料查找，资料分析和资料总结 |
| data-process-skill.md | 方法 | skills/official/data-process-skill.md | 是 | 用于数据清洗和数据分析 |
| plan-design-skill.md | 方法 | skills/official/plan-design-skill.md | 是 | 用于科研计划制定 |
| plan-implement-skill.md | 方法 | skills/official/plan-implement-skill.md | 是 | 用于计划执行 |
| result-handle-skill.md | 方法 | skills/official/result-handle-skill.md | 是 | 用于结果记录和结果总结 |
| python-program-skill.md | 方法 | skills/official/python-program-skill.md | 否 | 用于 Python 程序编写 |
| temp-file-handle-skill.md | 约束 | skills/official/temp-file-handle-skill.md | 否 | 用于临时文件的妥善处理 |