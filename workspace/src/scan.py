"""参数扫描工具"""

import numpy as np
import pandas as pd

from solver import solve_torsion, extract_period
from model import compute_inertia, theoretical_period
from config import SCAN_RANGES


def scan_parameter(param_name, param_values, fixed_params, t_span=20.0):
    """
    扫描单一参数，计算每个参数值下的振动周期。

    参数:
        param_name: 要扫描的参数名 ('k', 'm', 'c', 'theta0')
        param_values: 参数取值数组
        fixed_params: 固定参数字典
        t_span: 求解时长

    返回:
        DataFrame: 包含参数值、周期、理论周期等列
    """
    results = []
    I = compute_inertia(fixed_params.get('m', 0.01), fixed_params.get('R', 0.03))

    for val in param_values:
        # 构建当前参数集
        k = fixed_params.get('k', 0.05)
        c = fixed_params.get('c', 0.001)
        theta0 = fixed_params.get('theta0', 10.0)
        nonlinear = fixed_params.get('nonlinear', False)
        k3 = fixed_params.get('k3', 0.0)

        if param_name == 'k':
            k = val
        elif param_name == 'm':
            I = compute_inertia(val, fixed_params.get('R', 0.03))
        elif param_name == 'c':
            c = val
        elif param_name == 'theta0':
            theta0 = val

        try:
            t, y, info = solve_torsion(
                I=I, k=k, c=c, theta0=theta0,
                t_span=t_span, nonlinear=nonlinear, k3=k3
            )
            period = extract_period(t, y[0])
            T_theory = theoretical_period(I, k)

            results.append({
                param_name: val,
                'period': period if period else np.nan,
                'T_theory': T_theory,
                'energy_drift': float(np.std(info['energy'][-100:]) /
                                       np.mean(info['energy'][:100]))
                if np.mean(info['energy'][:100]) > 0 else np.nan,
            })
        except Exception as e:
            results.append({
                param_name: val,
                'period': np.nan,
                'T_theory': theoretical_period(I, k) if k > 0 else np.nan,
                'energy_drift': np.nan,
            })

    return pd.DataFrame(results)


def generate_scan_values(param_name):
    """根据配置生成参数扫描取值数组"""
    if param_name not in SCAN_RANGES:
        raise ValueError(f"未知参数: {param_name}")
    pmin, pmax, nsteps = SCAN_RANGES[param_name]
    return np.linspace(pmin, pmax, nsteps)


def scan_multiple_params(fixed_params, param_list=None):
    """
    扫描多个参数，返回参数字典。
    """
    if param_list is None:
        param_list = list(SCAN_RANGES.keys())

    results = {}
    for pname in param_list:
        values = generate_scan_values(pname)
        df = scan_parameter(pname, values, fixed_params)
        results[pname] = df

    return results
