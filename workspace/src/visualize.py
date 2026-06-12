"""数据可视化函数"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

from config import OUTPUT_DIR

# 中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Noto Sans SC']
plt.rcParams['axes.unicode_minus'] = False


def setup_plot_style():
    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 13,
        'axes.titlesize': 14,
        'legend.fontsize': 11,
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'figure.figsize': (10, 6),
    })


def _save_or_show(fig, save_path):
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
        plt.close(fig)
        return save_path
    plt.close(fig)
    return fig


def plot_time_response(t, y, I, k, c, theta0, save_path=None):
    setup_plot_style()
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    theta1, theta2 = y[0], y[1]
    omega1, omega2 = y[2], y[3]

    axes[0].plot(t, theta1, 'b-', label=r'$\theta_1$', linewidth=1.2)
    axes[0].plot(t, theta2, 'r--', label=r'$\theta_2$', linewidth=1.2)
    axes[0].set_ylabel('角度 [rad]')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].plot(t, omega1, 'b-', label=r'$\omega_1$', linewidth=1.2)
    axes[1].plot(t, omega2, 'r--', label=r'$\omega_2$', linewidth=1.2)
    axes[1].set_ylabel('角速度 [rad/s]')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)

    d_theta = theta1 - theta2
    axes[2].plot(t, d_theta, 'g-', label=r'$\Delta\theta$', linewidth=1.2)
    axes[2].set_xlabel('时间 [s]')
    axes[2].set_ylabel(r'$\Delta\theta$ [rad]')
    axes[2].legend(); axes[2].grid(True, alpha=0.3)

    fig.suptitle(f'扭振系统时域响应 ($\\theta_0$={theta0:.1f}rad, k={k:.3f}, c={c:.5f})')
    plt.tight_layout()
    return _save_or_show(fig, save_path)


def plot_phase_portrait(t, y, save_path=None):
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(8, 7))
    theta1, omega1 = y[0], y[2]
    sc = ax.scatter(theta1, omega1, c=t, s=1, cmap='viridis', alpha=0.7)
    ax.set_xlabel(r'$\theta_1$ [rad]')
    ax.set_ylabel(r'$\omega_1$ [rad/s]')
    ax.set_title('相空间轨迹')
    ax.grid(True, alpha=0.3)
    plt.colorbar(sc, ax=ax, label='时间 [s]')
    plt.tight_layout()
    return _save_or_show(fig, save_path)


def plot_parameter_scan(scan_results, save_path=None):
    setup_plot_style()
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    param_labels = {
        'k': '扭转刚度 k [N·m/rad]',
        'm': '小球质量 m [kg]',
        'c': '阻尼系数 c [N·m·s/rad]',
        'theta0': '初始扭转角 $\\theta_0$ [rad]',
    }
    for idx, (pname, df) in enumerate(scan_results.items()):
        if idx >= len(axes): break
        ax = axes[idx]
        x = df[pname].values
        period = df['period'].values
        T_theory = df['T_theory'].values
        valid = ~np.isnan(period)
        if np.any(valid):
            ax.plot(x[valid], period[valid], 'bo-', label='数值周期', markersize=4, linewidth=1.2)
        if pname != 'c':
            ax.plot(x, T_theory, 'r--', label='理论周期', linewidth=1.0, alpha=0.7)
        ax.set_xlabel(param_labels.get(pname, pname))
        ax.set_ylabel('周期 [s]')
        ax.set_title(f'周期 vs {pname}')
        ax.legend(); ax.grid(True, alpha=0.3)
    for idx in range(len(scan_results), len(axes)):
        axes[idx].set_visible(False)
    plt.tight_layout()
    return _save_or_show(fig, save_path)


def plot_nonlinear_comparison(t_linear, y_linear, t_nonlin, y_nonlin, theta0, save_path=None):
    setup_plot_style()
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    axes[0].plot(t_linear, y_linear[0], 'b-', label='线性模型', linewidth=1.2)
    axes[0].plot(t_nonlin, y_nonlin[0], 'r--', label='非线性Duffing', linewidth=1.2)
    axes[0].set_ylabel(r'$\theta_1$ [rad]')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)
    axes[1].plot(t_linear, y_linear[0] - y_linear[1], 'b-', label='线性模型', linewidth=1.2)
    axes[1].plot(t_nonlin, y_nonlin[0] - y_nonlin[1], 'r--', label='非线性Duffing', linewidth=1.2)
    axes[1].set_xlabel('时间 [s]')
    axes[1].set_ylabel(r'$\Delta\theta$ [rad]')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    fig.suptitle(f'线性 vs 非线性模型对比 ($\\theta_0$={theta0:.1f}rad)')
    plt.tight_layout()
    return _save_or_show(fig, save_path)


def plot_period_vs_amplitude(amplitudes, periods_linear, periods_nonlin, save_path=None):
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(8, 6))
    valid_lin = ~np.isnan(periods_linear)
    valid_nonlin = ~np.isnan(periods_nonlin)
    if np.any(valid_lin):
        ax.plot(amplitudes[valid_lin], periods_linear[valid_lin], 'bs-', label='线性模型', markersize=5, linewidth=1.5)
    if np.any(valid_nonlin):
        ax.plot(amplitudes[valid_nonlin], periods_nonlin[valid_nonlin], 'ro-', label='非线性Duffing', markersize=5, linewidth=1.5)
    ax.set_xlabel('初始振幅 [rad]')
    ax.set_ylabel('周期 [s]')
    ax.set_title('周期非等时性：周期 vs 初始振幅')
    ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return _save_or_show(fig, save_path)
