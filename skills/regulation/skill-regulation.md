# skill-regulation

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套在科研活动中进行 skill 管理的规范。

## 常规 skill 加载

### 1. 资料收集及整合

加载 `information-collect-method.md`。

### 2. 数据处理

加载 `data-process-method.md`。

### 3. 计划撰写

加载 `plan-design-method.md`。

### 4. 计划执行

加载 `plan-implement-method.md`。

### 5. 结果分析与验证

加载 `result-handle-method.md`。

---

## skill 管理

1. 在执行任何科研步骤之前，必须加载并严格遵守 `skills/regulation/` 中的 `...regulation.md` 文档记录的所有规则。
2. 同一个 skill 单轮任务最多加载一次。
3. Agent 不应读取或使用 `skill-index.md` 中没有提及的 skill。

---

## skill 矛盾处理

1. 如果两个 skill 的要求相互矛盾，应该向用户说明：
   - 两个 skill 各自的名称
   - 两个 skill 的哪两个要求自相矛盾
   同时为用户提供 `[A-skill/B-skill]` 选项：
   - 若用户选择 `A-skill`，遵从 `A-skill` 规则
   - 若用户选择 `B-skill`，遵从 `B-skill` 规则
