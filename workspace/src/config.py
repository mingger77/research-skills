"""默认参数配置（基于文献及实验估算）"""

import numpy as np

# 随机种子
RANDOM_SEED = 42

# 默认物理参数
DEFAULT_PARAMS = {
    'm': 0.01,          # 小球质量 [kg]（约10g，铜球）
    'R': 0.03,          # 公转半径 [m]（约3cm）
    'k': 0.05,          # 扭转刚度 [N·m/rad]（估算值）
    'c': 0.00005,       # 阻尼系数 [N·m·s/rad]（弱阻尼，ζ≈0.05）
    'theta0': 10.0,     # 初始扭转角 [rad]（约1.6圈）
    'nonlinear': False, # 是否使用非线性模型
    'k3': 0.0,          # 非线性刚度系数 [N·m/rad³]
}

# 参数扫描范围
SCAN_RANGES = {
    'k': (0.01, 0.2, 20),        # (min, max, steps)
    'm': (0.001, 0.05, 20),      # (min, max, steps)
    'c': (0.0, 0.0005, 15),      # (min, max, steps)
    'theta0': (1.0, 50.0, 15),   # (min, max, steps)
}

# 数值求解参数
SOLVER_CONFIG = {
    't_span': 20.0,      # 求解时长 [s]
    'dt': 0.001,         # 时间步长 [s]
    'method': 'RK45',    # ODE求解方法
    'rtol': 1e-8,        # 相对容差
    'atol': 1e-10,       # 绝对容差
}

# ===== 连续体波动模型参数 =====
WAVE_PARAMS = {
    'L': 0.12,           # 橡皮筋长度 [m]
    'G': 0.4e6,          # 剪切模量 [Pa]（橡胶典型值 0.4~0.8 MPa）
    'rho': 930,          # 密度 [kg/m³]（橡胶典型值 930 kg/m³）
    'sigma': 0.015,      # 初始高斯波包宽度 [m]
    'A': 1.0,            # 激励振幅 [rad]（驱动端边界用）
}

# 波动数值求解参数
WAVE_SOLVER = {
    'nx': 200,           # 空间网格点数
    'nt': 2000,          # 时间步数
    'CFL': 0.9,          # CFL 数（<1 保证稳定性）
    'bc_type': 'fixed',  # 边界类型: 'fixed' 两端固定, 'driven' 一端激励
}

# 驱动频率（用于 driven 边界条件）
DRIVE_FREQS = {
    'f1': None,          # 自动计算: 基频 f1 = v/(2L)
    'f2': None,          # 自动计算: 二阶 f2 = 2*f1
    'f3': None,          # 自动计算: 三阶 f3 = 3*f1
    'f4': None,          # 自动计算: 四阶 f4 = 4*f1
}

# 输出设置
OUTPUT_DIR = {
    'figures': 'workspace/result/figures/',
    'data': 'workspace/result/data/',
}
