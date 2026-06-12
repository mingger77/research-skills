# 实验运行日志

## Run 001 — Baseline仿真 + 参数扫描 + 非线性分析

| 项目 | 内容 |
|------|------|
| 时间 | 2026-06-12 |
| 随机种子 | 42 |
| Python版本 | 3.13.11 |
| numpy | 2.4.6 |
| scipy | 1.17.1 |
| matplotlib | 3.11.0 |
| pandas | 3.0.3 |

### 参数

```python
DEFAULT_PARAMS = {
    'm': 0.01,          # 小球质量 [kg]（约10g，铜球）
    'R': 0.03,          # 公转半径 [m]（约3cm）
    'k': 0.05,          # 扭转刚度 [N·m/rad]（估算值）
    'c': 5e-5,          # 阻尼系数 [N·m·s/rad]（弱阻尼，ζ≈0.05）
    'theta0': 10.0,     # 初始扭转角 [rad]（约1.6圈）
    'nonlinear': False, # 是否使用非线性模型
    'k3': 0.0,          # 非线性刚度系数 [N·m/rad³]
}
```

### 参数扫描范围

| 参数 | 范围 | 步数 |
|------|------|------|
| k (扭转刚度) | 0.01 ~ 0.2 N·m/rad | 20 |
| m (小球质量) | 0.001 ~ 0.05 kg | 20 |
| c (阻尼系数) | 0.0 ~ 0.0005 N·m·s/rad | 15 |
| θ₀ (初始扭转角) | 1.0 ~ 50.0 rad | 15 |

### 数据集版本

- 文献参数：基于立项报告及 IYPT 2022 相关论文估算
- 未使用实测数据（后续可替换）

---

## 输出文件清单

```
workspace/result/figures/
├── T1_baseline_undamped.png      # 无阻尼时域响应
├── T1_baseline_damped.png        # 有阻尼时域响应
├── T1_phase_portrait.png         # 相空间轨迹
├── T2_parameter_scan.png         # 四参数扫描汇总
├── T3_linear_vs_nonlinear.png    # 线性/非线性模型对比
└── T3_period_vs_amplitude.png    # 周期-振幅关系（非等时性）

workspace/result/data/
├── scan_k.csv                    # 刚度扫描数据
├── scan_m.csv                    # 质量扫描数据
├── scan_c.csv                    # 阻尼扫描数据
├── scan_theta0.csv               # 初始角扫描数据
├── period_vs_amplitude.csv       # 非等时性分析数据
└── driven_modes.csv              # 驱动端驻波模式数据
```

---

## Run 002 — 连续体波动模型 + 驻波分析

| 项目 | 内容 |
|------|------|
| 时间 | 2026-06-12 |
| 随机种子 | 42 |
| Python版本 | 3.13.11 |

### 波动模型参数

```python
WAVE_PARAMS = {
    'L': 0.12,           # 橡皮筋长度 [m]
    'G': 0.4e6,          # 剪切模量 [Pa]
    'rho': 930,          # 密度 [kg/m³]
}
WAVE_SOLVER = {
    'nx': 200,           # 空间网格
    'nt': 2000/4000,     # 时间步（固定/驱动）
    'CFL': 0.9,          # CFL 数
}
```

### 物理量

| 量 | 值 |
|---|-----|
| 波速 v = √(G/ρ) | 20.74 m/s |
| 基频 f₁ = v/(2L) | 86.41 Hz |
| 网格精度 dx | 6.03×10⁻⁴ m |
| 时间步 dt | 2.62×10⁻⁵ s |

### 驻波模式精度

| 模式 | 驱动频率 | 节点误差（最大） |
|:----:|:--------:|:--------------:|
| 1 | 86.4 Hz | -（边界激励检测困难）|
| 2 | 172.8 Hz | **0.03%** |
| 3 | 259.2 Hz | 3.9%（有伪节点）|
| 4 | 345.7 Hz | **1-2%** |

### 新增输出文件

```
workspace/result/figures/
├── T4_spacetime.png              # 传播时空图
├── T4_snapshot_initial.png       # 初始波形
├── T4_snapshot_final.png         # 最终波形
├── T4_standing_modes.png         # 驻波模式图
├── T4_wave_animation.gif         # 波动传播动画
├── T5_mode{1-4}_spacetime.png    # 各阶驱动时空图
├── T5_mode_comparison.png        # 模式对比
├── T5_frequency_response.png     # 频率响应
workspace/result/data/
└── driven_modes.csv              # 驱动模式数据
```
