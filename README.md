# Research-Skills

一套用于指导 AI Agent 进行科研工作的结构化 Skill 系统。

## 项目背景

本项目的前身是 [Research-with-Python-Skill](./previous-skills/Research-with-Python-Skill.md)，一个单体式 Skill 文件。在迭代过程中，原有的单体结构难以承载日益复杂的方法论体系，因此重构为当前的多层模块化架构——将规范、约束、方法三个层面分离，使职责更清晰、扩展更灵活。

## 项目结构

```
research-skills/
├── skills/
│   ├── regulation/         # 规范层：不可违背的元规则
│   │   ├── skill-regulation.md    # Skill 调用规范
│   │   ├── stage-regulation.md    # 状态管理规范
│   │   ├── project-regulation.md  # 项目结构规范
│   │   ├── action-regulation.md   # Agent 行为规范
│   │   └── language-regulation.md # 语言表达规范
│   ├── constraint/         # 约束层：特定场景的行为护栏
│   │   ├── data-process-constraint.md
│   │   ├── information-collect-constraint.md
│   │   ├── log-write-constraint.md
│   │   ├── plan-design-constraint.md
│   │   ├── report-write-constraint.md
│   │   └── result-write-constraint.md
│   ├── method/             # 方法层：具体操作指南
│   │   ├── data-process-method.md
│   │   ├── information-collect-method.md
│   │   ├── plan-design-method.md
│   │   ├── plan-implement-method.md
│   │   ├── python-program-method.md
│   │   ├── result-handle-method.md
│   │   └── temp-file-handle-method.md
│   ├── main.md             # 顶层调度
│   └── skill-index.md      # Skill 索引
├── examples/               # 使用示例（不公开）
├── previous-skills/        # 旧版 Skill（归档）
├── public-example/         # 公开示例（预留）
└── README.md               # 本文件
```

## 三层架构设计

| 层次 | 职责 | 特点 |
|------|------|------|
| **规范 (Regulation)** | 定义不可违背的元规则 | 全局适用，不可绕过 |
| **约束 (Constraint)** | 特定场景下的行为边界 | 按需加载，防止越界 |
| **方法 (Method)** | 具体操作步骤和实现指南 | 可执行，可迭代 |

## 科研工作流

系统将科研流程定义为以下状态机，严格按照顺序流转：

```
INIT
  → DIRECTION_DEFINED（方向确定）
  → INFORMATION_COLLECTING（资料收集及整合）
  → DATA_PROCESSING（数据处理）
  → PLAN_DESIGNING（计划撰写）
  → PLAN_IMPLEMENTING（计划执行）
  → ANALYZING（结果分析与验证）
  → COMPLETED（完成）
```

- 状态只能向前流转，除非用户明确要求回退或进入失败状态
- 每个阶段完成后向用户报告，等待确认后再推进
- 项目元数据和阶段日志自动维护，支持中断后恢复

## 核心设计原则

1. **安全 > 效率**：所有操作以安全为首要考量
2. **模块化**：规范、约束、方法三层分离，职责单一
3. **状态驱动**：科研流程由状态机驱动，按序推进
4. **可追溯**：每项结论必须标注可信度等级，可追溯到实验记录
5. **可复现**：固定随机种子、记录参数、版本化文件管理
6. **最小改动**：除非用户要求，否则不自动修改代码

## 许可协议

本项目基于 MIT 协议开源，详见 [LICENSE](./LICENSE) 文件。

## 鸣谢

感谢  **DeepSeek** 和 **ChatGPT** 为我的 skill 体系的编写提供了宝贵的意见

## 额外说明

本skill系统的开发是为了在大一年度项目上偷懒，现在，大一年度项目流产。不过，我又参加了暑假的课题组，该项目走向如何仍未可知。
