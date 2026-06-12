"""物理模型：扭振系统 ODE 右端函数"""

import numpy as np


def torsional_ode(t, x, I, k, c, nonlinear=False, k3=0.0):
    """
    二自由度扭振系统 ODE 右端函数。

    状态向量 x = [θ₁, θ₂, ω₁, ω₂]ᵀ

    参数:
        t: 时间 [s]
        x: 状态向量
        I: 转动惯量 [kg·m²] (I = m*R²)
        k: 扭转刚度 [N·m/rad]
        c: 阻尼系数 [N·m·s/rad]
        nonlinear: 是否使用非线性恢复力矩
        k3: 非线性刚度系数 [N·m/rad³]

    返回:
        dx/dt: 状态向量的时间导数
    """
    theta1, theta2, omega1, omega2 = x
    d_theta = theta1 - theta2
    d_omega = omega1 - omega2

    # 恢复力矩（可选非线性 Duffing 项）
    if nonlinear:
        T_restore = k * d_theta + k3 * d_theta ** 3
    else:
        T_restore = k * d_theta

    # 阻尼力矩
    T_damp = c * d_omega

    # 角加速度（两球大小相等、方向相反）
    alpha1 = -(T_restore + T_damp) / I
    alpha2 = (T_restore + T_damp) / I

    return [omega1, omega2, alpha1, alpha2]


def compute_inertia(m, R):
    """计算小球转动惯量 I = m * R²"""
    return m * R ** 2


def theoretical_period(I, k):
    """
    线性无阻尼系统的理论周期。
    相对扭转模式的固有圆频率 ω = sqrt(2k/I)，周期 T = 2π/ω。
    """
    if k <= 0 or I <= 0:
        return np.inf
    omega_n = np.sqrt(2 * k / I)
    return 2 * np.pi / omega_n


def total_energy(x, I, k):
    """
    计算系统总机械能（用于验证能量守恒）。
    E = 0.5 * I * (ω₁² + ω₂²) + 0.5 * k * (θ₁ - θ₂)²
    """
    theta1, theta2, omega1, omega2 = x
    KE = 0.5 * I * (omega1 ** 2 + omega2 ** 2)
    PE = 0.5 * k * (theta1 - theta2) ** 2
    return KE + PE
