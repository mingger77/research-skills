# project-regulation

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套可用于科研工作项目管理的规范。

## 结构规范

1. 文件改动位置限定在 `/workspace/` 中，除非用户硬性要求在 `/workspace/` 外的目录创建文件。
2. 必须向用户征询 `/workspace/` 是哪个目录，征询后：
   - 若用户未指定，则默认使用当前工作目录下的 `/workspace/`
   - 如果子目录不存在，Agent 应自动创建标准子目录结构（`data/raw/`, `data/processed/`, `docs/raw/` 等）
3. 将最终确定的 `/workspace/` 绝对路径记录在 `workspace/config.json` 中，供后续子 skill 读取。
4. 项目结构为：

   ```
   workspace/
   ├── data/
   │   ├── raw/
   │   ├── processed/
   │   └── result/
   ├── docs/
   │   ├── raw/
   │   ├── processed/
   │   ├── main/
   │   ├── result/
   │   └── log/
   ├── config.json
   ├── PROJECT_META.json
   ├── src/
   ├── env/       （可选）
   └── temp/      （可选）
   ```

---

## 文件规范

### 版本化文件原则

1. 对于需要迭代的文档（如计划、结果、报告），采用 **三位数字编号**：
     - `PLAN-001.md`, `PLAN-002.md`
     - `RESULT-001.md`, `RESULT-002.md`
     - `REPORT-001.md`, `REPORT-002.md`
2. 禁止使用 `_v2`, `_final`, `_new` 等模糊后缀。
3. 每次迭代生成新文件，不覆盖旧版本。
4. 当目标文件已存在且符合版本化命名规范时，Agent 应 **自动递增编号**（如 `PLAN-001.md` → `PLAN-002.md`），无需停止报告。

### 重复文件处理

1. 若由于 `action-regulation` 中的 **工作行为约束** 部分的小点 1 中的第 5 项停止工作时，行为如下：

   | 用户指令 | 对应操作             |
   | -------- | -------------------- |
   | 覆盖     | 覆盖原文件           |
   | 重命名   | 按指定新名称保存     |
   | 保留     | 跳过生成步骤并记录   |
