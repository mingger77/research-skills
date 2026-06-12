"""波动可视化：时空图、模式图、动画"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

from config import OUTPUT_DIR

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Noto Sans SC']
plt.rcParams['axes.unicode_minus'] = False


def _save_or_show(fig, save_path):
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
        plt.close(fig)
        return save_path
    plt.close(fig)
    return fig


def plot_spacetime(u, x, t, save_path=None):
    """绘制时空图：u(x,t) 的二维伪彩色图"""
    fig, ax = plt.subplots(figsize=(10, 7))
    extent = [x[0], x[-1], t[-1], t[0]]
    im = ax.imshow(u, aspect='auto', extent=extent, cmap='RdBu_r',
                   vmin=-np.abs(u).max(), vmax=np.abs(u).max())
    ax.set_xlabel('位置 x [m]')
    ax.set_ylabel('时间 t [s]')
    ax.set_title('波动传播时空图')
    plt.colorbar(im, ax=ax, label='振幅 u(x,t)')
    plt.tight_layout()
    return _save_or_show(fig, save_path)


def plot_snapshot(u, x, t, time_idx, label=None, save_path=None):
    """绘制某一时刻的波形快照"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, u[time_idx, :], 'b-', linewidth=1.5)
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlabel('位置 x [m]')
    ax.set_ylabel('振幅 u')
    ax.set_title(label or f'波形快照 (t={t[time_idx]:.4f}s)')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return _save_or_show(fig, save_path)


def plot_standing_wave_modes(u, x, t, n_modes=4, save_path=None):
    """
    绘制驻波模式（稳态后的波形）。
    通过对最后一段时间的波形做时间平均和归一化。
    """
    # 取后半段时间用于分析
    half = u.shape[0] // 2
    u_steady = u[half:, :]

    # 找到各阶模式：不同时刻的波形叠加
    fig, axes = plt.subplots(n_modes, 1, figsize=(10, 2.5 * n_modes), sharex=True)

    # 采样不同时间的波形来展示不同模式
    n_samples = u_steady.shape[0]
    for mode in range(n_modes):
        ax = axes[mode]
        # 在不同时间点采样，观察驻波包络
        for i in np.linspace(0, n_samples - 1, 8, dtype=int):
            ax.plot(x, u_steady[i, :], alpha=0.3, linewidth=0.8, color='blue')
        # 包络线（取绝对值的时间平均）
        envelope = np.mean(np.abs(u_steady[int(n_samples * 0.7):, :]), axis=0)
        ax.plot(x, envelope, 'r-', linewidth=1.5, label='振幅包络')
        ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
        ax.set_ylabel(f'模式 {mode + 1}')
        ax.grid(True, alpha=0.2)

    axes[-1].set_xlabel('位置 x [m]')
    axes[0].set_title('驻波模式（蓝色=不同时刻波形，红色=振幅包络）')
    axes[0].legend()
    plt.tight_layout()
    return _save_or_show(fig, save_path)


def plot_mode_comparison(x, nodes_list, L, save_path=None):
    """
    绘制驻波节点位置与理论值对比。
    nodes_list: [(mode_label, nodes_array), ...]
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['blue', 'red', 'green', 'orange']
    for idx, (label, nodes) in enumerate(nodes_list):
        if nodes is None or len(nodes) == 0:
            continue
        c = colors[idx % len(colors)]
        ax.scatter(nodes, np.full_like(nodes, idx), c=c, label=label, s=30)

    ax.set_xlabel('位置 x [m]')
    ax.set_ylabel('模式')
    ax.set_title('驻波节点位置：数值 vs 理论')
    ax.set_xlim(0, L)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return _save_or_show(fig, save_path)


def create_wave_animation(u, x, t, save_path=None, fps=30):
    """生成波动传播动画 GIF"""
    fig, ax = plt.subplots(figsize=(10, 5))

    line, = ax.plot(x, u[0, :], 'b-', linewidth=1.5)
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlabel('位置 x [m]')
    ax.set_ylabel('振幅 u')
    ax.set_title(f'波动传播 (t={t[0]:.4f}s)')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-np.abs(u).max() * 1.1, np.abs(u).max() * 1.1)

    def update(frame):
        line.set_ydata(u[frame, :])
        ax.set_title(f'波动传播 (t={t[frame]:.4f}s)')
        return line,

    # 降采样帧数以控制文件大小
    step = max(1, u.shape[0] // 200)
    frames = range(0, u.shape[0], step)

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / fps, blit=True)

    if save_path:
        anim.save(save_path, writer='pillow', fps=fps)
        plt.close(fig)
        return save_path

    plt.close(fig)
    return anim
