"""数值求解器封装"""

import numpy as np
from scipy.integrate import solve_ivp

from model import torsional_ode, compute_inertia, theoretical_period, total_energy
from config import SOLVER_CONFIG


def solve_torsion(I, k, c, theta0, t_span=None, dt=None,
                  method=None, rtol=None, atol=None,
                  nonlinear=False, k3=0.0):
    """
    求解二自由度扭振系统 ODE。

    参数:
        I: 转动惯量 [kg·m²]
        k: 扭转刚度 [N·m/rad]
        c: 阻尼系数 [N·m·s/rad]
        theta0: 初始扭转角 [rad]
        t_span: 求解时长 [s]
        dt: 时间步长 [s]
        method: ODE求解方法
        nonlinear: 是否使用非线性模型
        k3: 非线性刚度系数

    返回:
        t: 时间序列
        y: 状态序列 [θ₁, θ₂, ω₁, ω₂]
        info: 附加信息字典
    """
    if t_span is None:
        t_span = SOLVER_CONFIG['t_span']
    if dt is None:
        dt = SOLVER_CONFIG['dt']
    if method is None:
        method = SOLVER_CONFIG['method']
    if rtol is None:
        rtol = SOLVER_CONFIG['rtol']
    if atol is None:
        atol = SOLVER_CONFIG['atol']

    # 初始条件：两球反向扭转相同角度，初始角速度为零
    x0 = [theta0, -theta0, 0.0, 0.0]

    t_eval = np.arange(0, t_span, dt)

    sol = solve_ivp(
        torsional_ode,
        [0, t_span],
        x0,
        args=(I, k, c, nonlinear, k3),
        t_eval=t_eval,
        method=method,
        rtol=rtol,
        atol=atol,
    )

    if not sol.success:
        raise RuntimeError(f"ODE求解失败: {sol.message}")

    # 计算能量
    energy = np.array([total_energy(sol.y[:, i], I, k)
                       for i in range(len(sol.t))])

    T_theory = theoretical_period(I, k)

    info = {
        'success': sol.success,
        'n_eval': len(sol.t),
        't_span': t_span,
        'energy': energy,
        'T_theory': T_theory,
    }

    return sol.t, sol.y, info


def extract_period(t, theta, min_peaks=3):
    """
    从角度时间序列中提取振动周期（过零点检测法）。

    返回: 平均周期，若无法检测返回 None
    """
    # 寻找符号变化（从正到负）
    signs = np.sign(theta)
    zero_crossings = np.where(np.diff(signs) < 0)[0]

    if len(zero_crossings) < min_peaks:
        return None

    # 计算相邻过零点的时间差
    crossing_times = t[zero_crossings]
    periods = np.diff(crossing_times)

    # 去除离群值（超出中位数 ±50%）
    median_period = np.median(periods)
    valid = periods[periods < median_period * 1.5]
    valid = valid[valid > median_period * 0.5]

    if len(valid) < 1:
        return None

    return float(np.mean(valid))


def extract_period_zero_crossing(t, theta):
    """
    一种更稳健的周期提取：线性插值法找过零点。
    """
    # 找到所有过零点（包含从负到正和从正到负）
    zero_times = []
    for i in range(len(t) - 1):
        if theta[i] == 0:
            zero_times.append(t[i])
        elif theta[i] * theta[i + 1] < 0:
            # 线性插值
            t1, t2 = t[i], t[i + 1]
            y1, y2 = theta[i], theta[i + 1]
            t_zero = t1 - y1 * (t2 - t1) / (y2 - y1)
            zero_times.append(t_zero)

    zero_times = np.array(zero_times)

    if len(zero_times) < 4:
        return None

    # 半周期 = 相邻过零点间隔，全周期 = 每两个间隔之和
    half_periods = np.diff(zero_times)

    # 取所有偶数间隔（全周期）的平均值
    if len(half_periods) >= 2:
        full_periods = half_periods[0::2] + half_periods[1::2]
        if len(full_periods) > 0:
            return float(np.mean(full_periods))

    return None
