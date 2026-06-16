# python-program-skill

这个 skill 旨在给以 Claude Code 为代表的 Agent 提供一套可用于在科研中进行 Python 程序编写的方法论。

## Python 程序编写

1. **虚拟环境准备**：
   - 默认在 `/workspace/env` 创建 venv；若用户要求 conda 则询问环境名
   - 使用 **清华源** 安装依赖（`-i https://pypi.tuna.tsinghua.edu.cn/simple`）
   - 若依赖安装失败，停止并报告
2. **程序编写及运行**：
   - 创建相应的 Python 文件
   - 运行程序，将结果放在 `/result/` 中
   - 针对 Python 文件及其结果编写解析文档
3. **Python 代码要求**：
   - 必须拆分函数
   - 必须包含必要注释
   - 必须提供 `src/requirements.txt`
   - 必须提供运行说明
   - 必须固定随机数种子
4. 除非用户要求，否则 **不自动修改代码**，只报告问题。