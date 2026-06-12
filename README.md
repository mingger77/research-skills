# Research-with-Python-Skill

顾名思义，**Research-with-Python-Skill** 是一个用于指导 Agent 利用 Python 进行科研工作的 Skill。

## 项目背景

这事说来颇具戏剧性：大一年度项目，室友选了我不感兴趣的物理课题。
我不感兴趣，但也不想无所作为，于是决定把实验流程交给 AI 来处理。我花了几小时写了这个 Skill —— 让 Agent 按科研规范自动执行仿真、记录实验、生成报告。

## 项目结构

```
Research-with-Python-Skill/
├── Research-with-Python-Skill.md  # Skill 核心正文（总纲 + 准备篇 + 实行篇）
├── workspace/                     # 使用该 Skill 时的实际工作目录
├── .claude/                       # Claude Code 自动生成的配置目录
└── README.md                      # 本文件
```

## 核心内容

1. **Research-with-Python-Skill.md**

   包含：
   - **总纲**（7 条）：行为准则、停止机制、迭代上限等
   - **准备篇**（3 大板块，11 条）：方向确定、资料整合、计划撰写
   - **实行篇**（2 大板块，9 条）：Python 编程、结果分析与验证

   详细内容见 `Research-with-Python-Skill.md`。

2. **workspace/**

   我使用该 Skill 指导 Claude Code 进行科研工作时生成的工作目录，用于证明本 Skill 的有效性。

   绝大多数内容由 Claude Code 完成，我只做了少量无关修改。

## 成果

| 指标 | 数据 |
|------|------|
| 课题 | 橡皮筋弹性驻波仿真 |
| API 费用 | **0.46 元** |
| Token 消耗 | 850 万 |
| 产出 | 2 轮实验、9 个 Python 模块、18 张图、1 个动画、6 个 CSV、8 份文档 |
完整的实验报告参见 [REPORT.md](./workspace/docs/REPORT.md)

## 附录

1. 为保护隐私，仅展示少量数据，所有涉及隐私的内容均已匿名化处理。
2. 本 Skill 的编写离不开 `DeepSeek` 和 `ChatGPT` 的帮助。
3. 本 Skill 为初版，尚有诸多不完善之处，敬请包涵。
