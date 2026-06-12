"""驻波模式分析：频率提取、节点检测、理论对比"""

import numpy as np
import pandas as pd


def detect_standing_waves(u, x, t, n_modes=4):
    """
    检测驻波模式，返回各模式的频率和节点位置。

    参数:
        u: 波函数矩阵 [nt, nx]
        x: 空间坐标
        t: 时间序列
        n_modes: 检测的模式数量

    返回:
        modes: [(freq, nodes), ...] 各模式的频率和节点位置
    """
    nt, nx = u.shape
    dt = t[1] - t[0]
    dx = x[1] - x[0]

    # 取中心点的时域信号做 FFT
    center_idx = nx // 2
    signal = u[:, center_idx]

    # FFT 分析
    freqs = np.fft.rfftfreq(nt, dt)
    spectrum = np.abs(np.fft.rfft(signal))

    # 找前 n_modes 个峰值（避开直流）
    peak_indices = _find_peaks(spectrum, n_modes)

    modes = []
    for idx in peak_indices:
        if idx > 0:
            freq = freqs[idx]
            # 对该频率做窄带滤波
            filtered = _bandpass_filter(u, dt, freq, bandwidth=freq * 0.1)
            # 检测节点
            nodes = _find_nodes_from_snapshot(filtered, x, t)
            modes.append((freq, nodes))

    return modes


def _find_peaks(spectrum, n_peaks):
    """找到频谱中前 n_peaks 个峰值"""
    # 忽略 DC 分量和过低幅度
    min_amp = np.max(spectrum) * 0.05
    candidates = []

    # 简单峰值检测：比相邻点都大
    for i in range(2, len(spectrum) - 2):
        if (spectrum[i] > spectrum[i - 1] and
            spectrum[i] > spectrum[i + 1] and
            spectrum[i] > min_amp):
            candidates.append((spectrum[i], i))

    candidates.sort(reverse=True)
    return [idx for _, idx in candidates[:n_peaks]]


def _bandpass_filter(u, dt, center_freq, bandwidth=None):
    """
    对波函数做窄带滤波（频域矩形窗），保留指定频率附近的成分。
    """
    nt, nx = u.shape
    if bandwidth is None:
        bandwidth = center_freq * 0.1

    freqs = np.fft.fftfreq(nt, dt)
    mask = np.abs(np.abs(freqs) - center_freq) < bandwidth

    filtered = np.zeros_like(u)
    for i in range(nx):
        F = np.fft.fft(u[:, i])
        F[~mask] = 0
        filtered[:, i] = np.fft.ifft(F).real

    return filtered


def _find_nodes_from_snapshot(filtered, x, t):
    """
    从滤波后的波函数中检测节点位置。
    使用时间平均的过零点。
    """
    # 取后半段，已形成稳态
    half = filtered.shape[0] // 2
    steady = filtered[half:, :]

    # 时间平均
    avg = np.mean(steady, axis=0)
    avg -= np.mean(avg)

    # 过零点检测
    nodes = []
    for i in range(len(avg) - 1):
        if avg[i] * avg[i + 1] < 0:
            x_node = x[i] - avg[i] * (x[i + 1] - x[i]) / (avg[i + 1] - avg[i])
            nodes.append(x_node)

    return np.array(nodes)


def theoretical_nodes(n, L):
    """
    计算第 n 阶驻波的理论节点位置。
    两端固定弦：x_j = j * L / n, j=0,1,...,n
    返回不含端点的节点数组。
    """
    nodes = np.array([j * L / n for j in range(1, n)])
    return nodes


def theoretical_frequency(n, L, G, rho):
    """计算第 n 阶驻波的理论频率 f_n = n * v / (2L)"""
    from wave_model import wave_speed
    v = wave_speed(G, rho)
    return n * v / (2 * L)


def compute_frequency_scan(u, x, t):
    """
    在驱动端边界条件下，对波函数各空间点的频谱做平均，
    得到系统的共振频率。
    """
    nt, nx = u.shape
    dt = t[1] - t[0]
    freqs = np.fft.rfftfreq(nt, dt)

    # 对各点的频谱做平均
    spectrum_sum = np.zeros(len(freqs))
    for i in range(nx):
        spectrum_sum += np.abs(np.fft.rfft(u[:, i]))

    spectrum_sum /= nx

    return freqs, spectrum_sum


def node_error(nodes_numerical, nodes_theoretical):
    """
    计算数值节点位置与理论值的误差。
    """
    if len(nodes_numerical) == 0 or len(nodes_theoretical) == 0:
        return None
    # 确保数量一致
    n = min(len(nodes_numerical), len(nodes_theoretical))
    errors = np.abs(nodes_numerical[:n] - nodes_theoretical[:n])
    return {
        'mean_error': float(np.mean(errors)),
        'max_error': float(np.max(errors)),
        'rms_error': float(np.sqrt(np.mean(errors ** 2))),
    }
