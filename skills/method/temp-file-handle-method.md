# temp-file-handle-method

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套关于如何处理临时文件的规定。

---

## 临时程序运行

### 1. 创建前告知

在正式创建临时程序之前，向用户说明：

- 创建临时程序的原因
- 临时程序的作用
- 是否需要保留该临时文件供调试（若不保留，将在任务完成后自动清理）

### 2. 创建临时目录

创建目录 `workspace/temp/`（如已存在则跳过）。

### 3. 创建临时程序

在 `temp/` 中创建所需的 Python 程序：

- 命名规范：`temp_<用途>_<YYYYMMDD_HHMM>.py`，例如 `temp_clean_20260615_1430.py`
- 代码编写规范参见 `skills/official/python-program-method.md`

### 4. 记录创建信息

将临时文件的创建信息记录到 `workspace/docs/log/EXECUTION_LOG.md`，包括：

- 文件名、原因、作用、创建时间

### 5. 任务完成后的处理

- 若用户要求保留，则将文件移动到 `workspace/temp/archive/`（自动创建该目录）并记录路径
- 否则，删除该临时文件及同次任务生成的其它临时数据
- 若删除失败，将错误信息记入日志，并向用户报告，不自动重试

### 6. 清理记录

清理完成后，在日志中记录清理结果。
