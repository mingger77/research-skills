# skill-index

这个索引旨在给以 Claude Code 为代表的 Agent 提供一个关于指导 Agent 进行科研活动的一系列 skill 的索引。

## skill 大体位置结构

   ```
   skills/
   ├── regulation/			# 存放“规范”类 skill
   ├── constraint/			# 存放“约束”类 skill
   ├── method/			    # 存放“方法”类 skill
   ├── main.md				# 主 skill
   └── skill-index.md		# skill 索引
   ```

## 独立文档说明

根目录下存在 main.md（顶层调度）和 skill-index.md（本文件），不作为 method/constraint/regulation 分类。

## 正式索引

### 规范类 skill 索引

**skill 位置**： `research-skills/skills/regulation/`

**位置结构**：

   ```
   regulation/					# 底层规范（不可违背的元规则）
   ├── skill-regulation.md		# 用于规范 skill 调用
   ├── stage-regulation.md		# 用于规范状态管理
   ├── project-regulation.md	# 用于规范项目结构
   ├── action-regulation.md		# 用于规范 Agent 行为
   └── language-regulation.md	# 用于规范语言表达
   ```


### 方法类 skill 索引

**skill 位置**： `research-skills/skills/method/` 

**位置结构**：

   ```
   method/								# 具体操作方法（执行层）
   ├── data-process-method.md			# 用于数据处理
   ├── information-collect-method.md	# 用于资料收集
   ├── plan-design-method.md			# 用于计划设计
   ├── plan-implement-method.md			# 用于计划执行
   ├── python-program-method.md			# 用于 Python 程序编写
   ├── result-handle-method.md			# 用于结果处理
   └── temp-file-handle-method.md		# 用于临时文件处理
   ```

### 约束类 skill 索引

**skill 位置**： `research-skills/skills/constraint` 

**位置结构**：

   ```
   constraint/								# 行为约束（特定场景的护栏）
   ├── information-collect-constraint.md	# 用于约束信息收集方法
   ├── log-write-constraint.md				# 用于约束日志记录
   ├── plan-design-constraint.md			# 用于约束计划设计
   ├── report-write-constraint.md			# 用于约束报告撰写
   └── result-write-constraint.md			# 用于约束结果编写
   ```
