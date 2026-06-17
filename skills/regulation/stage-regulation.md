# stage-regulation

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套在科研活动中进行状态管理的规范。

### 状态映射规则

| 步骤             | 状态                  |
| ---------------- | --------------------- |
| 方向确定         | DIRECTION_DEFINED                  |
| 资料收集及整合   | INFORMATION_COLLECTING     |
| 数据处理         | DATA_PROCESSING        |
| 计划撰写         | PLAN_DESIGNING        |
| 计划执行         | PLAN_IMPLEMENTING     |
| 结果分析与验证   | ANALYZING             |

## 状态流转规则

1. 状态只能按以下顺序向前流转：
   `INIT` → `DIRECTION_DEFINED` → `INFORMATION_COLLECTING` → `DATA_PROCESSING` → `PLAN_DESIGING` → `PLAN_IMPLEMENTING` → `ANALYZING` → `COMPLETED`
2. 在进行科研工作时，Agent 应该：
   - 从上一个状态向下一状态流转，但以下情况除外：
     - 用户明确要求回退
     - 科研工作进入失败状态
   - 待报告完成后，为用户提供 `[yes/no]` 选项：
     - 若用户选择 `yes`，推进下一步
     - 若用户选择 `no`，不得推进下一步
3. 根据 `action-regulation.md` 中的停止机制（正常完成 / 需要决策），向用户报告并等待指示。
4. 待报告完成后，为用户提供 `[yes/no]` 选项：
   - 若用户选择 `yes`，推进下一步
   - 若用户选择 `no`，不得推进下一步
5. Agent 不得跳过科研流程中的任意阶段，除非：
   - 用户明确要求跳过
   - 当前阶段已经完成并存在对应文档

## 状态记录规则

1. 创建 `workspace/PROJECT_META.json`，文件内容格式如下：

```json
{
  "project_name": "未命名科研项目",
  "research_direction": "待用户确认",
  "research_goal": "待用户确认",
  "current_state": "INIT",
  "current_plan": null,
  "active_plan": null,
  "created_time": null,
  "created_location": null,
  "last_updated_time": null
}
```

2. 参考 `log-write-constraint`，创建日志 `STAGE_LOG.md`
3. 每个阶段完成后，必须更新：
   - `PROJECT_META.json`
   - `STAGE_LOG.md`

## 状态恢复规则

1. Agent 启动时，检查 `PROJECT_META.json`：
   - 如果不存在，回到 **状态记录** 步骤
   - 如果存在，应该：
     - 向用户报告 `PROJECT_META.json` 中全部内容
     - 为用户提供 `[yes/no]` 选项，根据用户选择来决定是否推进下一步