# main

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套进行科研活动的方法论。

**总原则：安全 > 效率**

**使用场景说明**：本 skill 及所有子 skill 适用于 **探索性科研编程任务**，不适用于生产环境部署或实时系统。

---

## 概况

### 1. 科研介绍

科研的一般步骤为：
   **方向确定** → **资料收集及整合** → **数据处理** → **计划撰写** → **计划执行** → **结果分析与验证**

### 2. 项目结构

项目结构如下：

```
research-skills/
├── examples/              # 示例
├── skills/                # 方法
├── README.md              # 说明文档
└── previous-skills/       # 存放旧版本 skill 的文件，忽略之
```

---

## 科研执行

### 重要 skill 加载

1. 在 `main.md` 被加载后，应该立即：
   - 加载 `skill-index.md`
   - 缓存所有技能的位置、类别、是否必须调用等信息
   - 在执行 "skill 加载规范" 时，根据该索引进行判断
2. 在 `skill-index.md` 被加载后，加载
   - `stage-regulation.md`
   - `project-regulation.md`
   - `action-regulation.md`
   - `language-regulation.md`

### 2. 方向确定

在正式开始工作之前，向用户询问以下信息：
   - 用户的研究方向
   - 用户的科研目标
   - 用户是否有相关领域的资料

### 3.进行其余步骤




