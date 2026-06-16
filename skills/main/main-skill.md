# main-skill

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套进行科研活动的方法论。

**总原则：安全 > 效率**

**使用场景说明**：本 skill 及所有子 skill 适用于 **探索性科研编程任务**，不适用于生产环境部署或实时系统。

---

## 概况

1. **科研介绍**
科研的一般步骤为：
   - 方向确定
   - 资料收集及整合
   - 计划撰写
   - 计划执行
   - 结果分析与验证

2. **方向确定**
在正式开始工作之前，向用户询问以下信息：
   - 用户的研究方向
   - 用户的科研目标
   - 用户是否有相关领域的资料

3. **项目结构**
项目结构如下：

   ```
   research-skills/
   ├── examples/ # 示例
   ├── skills/ # skill仓库
   │   ├── main/
   │   ├── official/
   │   └── contributed/
   ├── README.md # 说明文档
   └── previous-skills/ # 存放旧版本 skill 的文件，忽略之
   ```

3. **skill 认识**
加载 `skill-index.md`

## skill 加载规范

1. 在 `skill-index.md` 中 **是否必须调用** 指标为 ”是“ 的 skill 必须加载
2. 在 `skill-index.md` 中 **是否必须调用** 指标为 ”否“ 的 skill 加载时一定要向用户说明
3. 在 `skill-index.md` 中 **位置** 指标为 `skills/contributed/...-skill.md` 的 skill 前，应该：
   - 停止当前工作
   - 向用户说明必要性
   - 征得用户同意后调用 skill
4. Agent 不应读取或使用 previous-skills/ 中的任何文件

