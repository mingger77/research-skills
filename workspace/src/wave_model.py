"""一维波动方程有限差分求解 (FTCS 显式格式)"""

import numpy as np


def wave_speed(G, rho):
    """计算扭转波速 v = sqrt(G/rho)"""
    return np.sqrt(G / rho)


def compute_dt(dx, v, CFL=0.9):
    """根据 CFL 条件计算时间步长"""
    return CFL * dx / v


def solve_wave_equation(L, G, rho, nx=200, nt=2000, CFL=0.9,
                         bc_type='fixed', excitation=None,
                         initial_condition='gaussian'):
    """
    有限差分法求解一维波动方程 ∂²u/∂t² = v² · ∂²u/∂x²

    参数:
        L: 橡皮筋长度 [m]
        G: 剪切模量 [Pa]
        rho: 密度 [kg/m³]
        nx: 空间网格点数
        nt: 时间步数
        CFL: CFL 数（<1 保证稳定性）
        bc_type: 'fixed' 两端固定, 'driven' 一端激励
        excitation: 函数 (t) -> 驱动端位移（仅 driven 模式）
        initial_condition: 'gaussian' 高斯波包, 'zero' 零初始条件

    返回:
        u: 波函数矩阵 [nt, nx]
        x: 空间坐标 [nx]
        t: 时间序列 [nt]
        dt: 时间步长
        dx: 空间步长
    """
    dx = L / (nx - 1)
    v = wave_speed(G, rho)
    dt = compute_dt(dx, v, CFL)
    r = (v * dt / dx) ** 2  # CFL² 用于差分公式

    # 波函数矩阵 u[n, i] = u(x_i, t_n)
    u = np.zeros((nt, nx))
    x = np.linspace(0, L, nx)

    # 初始条件
    if initial_condition == 'gaussian':
        sigma = L / 8
        x0 = L / 2
        u[0, :] = np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))
        # 第二步使用欧拉法
        u[1, 1:-1] = u[0, 1:-1]  # 零初始速度
    elif initial_condition == 'impulse':
        # 脉冲：只在中间点有位移
        u[0, :] = 0
        u[0, nx // 2] = 1.0
        u[1, 1:-1] = u[0, 1:-1]
    else:
        # 零初始条件（用于驱动端边界）
        pass

    # 应用边界条件（时间步 0）
    if bc_type == 'fixed':
        u[:, 0] = 0
        u[:, -1] = 0
    elif bc_type == 'driven' and excitation:
        u[0, 0] = excitation(0)

    # 时间推进
    for n in range(1, nt - 1):
        # 内部点：FTCS 差分
        u[n + 1, 1:-1] = (2 * u[n, 1:-1] - u[n - 1, 1:-1]
                          + r * (u[n, 2:] - 2 * u[n, 1:-1] + u[n, :-2]))

        # 边界条件
        if bc_type == 'fixed':
            u[n + 1, 0] = 0
            u[n + 1, -1] = 0
        elif bc_type == 'driven':
            if excitation:
                u[n + 1, 0] = excitation((n + 1) * dt)
            u[n + 1, -1] = 0

    # 如果用了大量时间步，裁剪实际使用的行
    t = np.arange(nt) * dt

    return u, x, t, dt, dx


def compute_energy(u, dx, v):
    """
    计算波动系统的总能量（用于验证能量守恒）。
    E(t) = 0.5 * Σ [(du/dt)² + v² * (du/dx)²] * dx
    """
    nt, nx = u.shape
    energy = np.zeros(nt)
    for n in range(nt):
        du_dt = np.gradient(u[n, :], dx)
        du_dx = np.gradient(u[n, :], dx)
        energy[n] = 0.5 * np.sum(du_dt ** 2 + v ** 2 * du_dx ** 2) * dx
    return energy


def find_nodes(u, x, threshold=0.05):
    """
    检测驻波节点位置（波函数长时间平均的零点）。
    返回节点位置列表。
    """
    # 时间平均
    u_avg = np.mean(u[-int(u.shape[0] * 0.3):, :], axis=0)
    u_avg -= np.mean(u_avg)  # 去直流

    # 过零点检测
    nodes = []
    for i in range(len(u_avg) - 1):
        if u_avg[i] * u_avg[i + 1] < 0:
            # 线性插值
            x_node = x[i] - u_avg[i] * (x[i + 1] - x[i]) / (u_avg[i + 1] - u_avg[i])
            nodes.append(x_node)

    return np.array(nodes)
