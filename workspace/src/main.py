"""主入口：运行所有仿真并输出结果"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DEFAULT_PARAMS, SOLVER_CONFIG, OUTPUT_DIR, RANDOM_SEED, WAVE_PARAMS, WAVE_SOLVER
from model import compute_inertia, theoretical_period
from solver import solve_torsion, extract_period
from scan import generate_scan_values, scan_parameter
from visualize import (plot_time_response, plot_phase_portrait,
                       plot_parameter_scan, plot_nonlinear_comparison,
                       plot_period_vs_amplitude)
from wave_model import solve_wave_equation, compute_energy, find_nodes, wave_speed
from wave_analyze import (theoretical_nodes, theoretical_frequency,
                           detect_standing_waves, node_error)
from wave_visualize import (plot_spacetime, plot_snapshot,
                             plot_standing_wave_modes, create_wave_animation)
import pandas as pd


def ensure_dirs():
    for d in OUTPUT_DIR.values():
        os.makedirs(d, exist_ok=True)


def run_baseline(params):
    print("=" * 50)
    print("T1: Baseline ODE Solver Validation")
    print("=" * 50)

    I = compute_inertia(params['m'], params['R'])
    print(f"  Moment of inertia I = {I:.6e} kg-m^2")
    print(f"  Theoretical period  T = {theoretical_period(I, params['k']):.4f} s")

    # Undamped: verify energy conservation
    print("\n>> Undamped case (energy conservation check)...")
    t, y, info = solve_torsion(
        I=I, k=params['k'], c=0.0, theta0=params['theta0'],
        t_span=SOLVER_CONFIG['t_span'], dt=SOLVER_CONFIG['dt']
    )
    period = extract_period(t, y[0])
    T_theory = theoretical_period(I, params['k'])
    energy_std = np.std(info['energy'])
    energy_mean = np.mean(info['energy'])
    print(f"  Numerical period  T_num = {period:.4f} s")
    print(f"  Error: {abs(period - T_theory) / T_theory * 100:.3f}%")
    print(f"  Energy drift: {energy_std:.6e} (mean={energy_mean:.6f})")

    plot_time_response(t, y, I, params['k'], 0.0, params['theta0'],
                       save_path=os.path.join(OUTPUT_DIR['figures'], 'T1_baseline_undamped.png'))

    # Damped case
    print(f"\n>> Damped case (c={params['c']})...")
    t_d, y_d, info_d = solve_torsion(
        I=I, k=params['k'], c=params['c'], theta0=params['theta0'],
        t_span=SOLVER_CONFIG['t_span'], dt=SOLVER_CONFIG['dt']
    )
    period_d = extract_period(t_d, y_d[0])
    print(f"  Numerical period T_num = {period_d:.4f} s" if period_d else "  No oscillation (overdamped)")

    plot_time_response(t_d, y_d, I, params['k'], params['c'], params['theta0'],
                       save_path=os.path.join(OUTPUT_DIR['figures'], 'T1_baseline_damped.png'))
    plot_phase_portrait(t_d, y_d, save_path=os.path.join(OUTPUT_DIR['figures'], 'T1_phase_portrait.png'))

    print("T1 done.\n")
    return I


def run_parameter_scan(params, I):
    print("=" * 50)
    print("T2: Parameter Scan")
    print("=" * 50)

    fixed_params = {'m': params['m'], 'R': params['R'], 'k': params['k'],
                    'c': params['c'], 'theta0': params['theta0']}
    scan_results = {}

    for pname in ['k', 'm', 'c', 'theta0']:
        print(f"  Scanning {pname} ...", end=' ')
        values = generate_scan_values(pname)
        df = scan_parameter(pname, values, fixed_params, t_span=SOLVER_CONFIG['t_span'])
        scan_results[pname] = df
        valid = df['period'].dropna()
        print(f"{len(valid)}/{len(df)} valid points")

    plot_parameter_scan(scan_results,
                        save_path=os.path.join(OUTPUT_DIR['figures'], 'T2_parameter_scan.png'))
    for pname, df in scan_results.items():
        df.to_csv(os.path.join(OUTPUT_DIR['data'], f'scan_{pname}.csv'), index=False)

    print("T2 done.\n")
    return scan_results


def run_nonlinear_analysis(params, I):
    print("=" * 50)
    print("T3: Period Non-isochronism Analysis")
    print("=" * 50)

    amplitudes = np.linspace(1.0, 50.0, 15)
    k3 = params['k'] / 100  # soft spring: period increases with amplitude
    periods_linear, periods_nonlin = [], []

    periods_linear, periods_nonlin = [], []
    for amp in amplitudes:
        t_lin, y_lin, _ = solve_torsion(I=I, k=params['k'], c=0.0, theta0=amp,
                                         t_span=SOLVER_CONFIG['t_span'], dt=SOLVER_CONFIG['dt'],
                                         nonlinear=False)
        t_nl, y_nl, _ = solve_torsion(I=I, k=params['k'], c=0.0, theta0=amp,
                                       t_span=SOLVER_CONFIG['t_span'], dt=SOLVER_CONFIG['dt'],
                                       nonlinear=True, k3=k3)
        p_lin = extract_period(t_lin, y_lin[0])
        p_nl = extract_period(t_nl, y_nl[0])
        periods_linear.append(p_lin if p_lin else np.nan)
        periods_nonlin.append(p_nl if p_nl else np.nan)

    amplitudes = np.array(amplitudes)
    periods_linear = np.array(periods_linear)
    periods_nonlin = np.array(periods_nonlin)

    plot_period_vs_amplitude(amplitudes, periods_linear, periods_nonlin,
                             save_path=os.path.join(OUTPUT_DIR['figures'], 'T3_period_vs_amplitude.png'))

    mid_amp = 20.0
    t_lin, y_lin, _ = solve_torsion(I=I, k=params['k'], c=0.0, theta0=mid_amp,
                                     t_span=SOLVER_CONFIG['t_span'], dt=SOLVER_CONFIG['dt'],
                                     nonlinear=False)
    t_nl, y_nl, _ = solve_torsion(I=I, k=params['k'], c=0.0, theta0=mid_amp,
                                    t_span=SOLVER_CONFIG['t_span'], dt=SOLVER_CONFIG['dt'],
                                    nonlinear=True, k3=k3)
    plot_nonlinear_comparison(t_lin, y_lin, t_nl, y_nl, mid_amp,
                              save_path=os.path.join(OUTPUT_DIR['figures'], 'T3_linear_vs_nonlinear.png'))

    pd.DataFrame({'amplitude': amplitudes, 'period_linear': periods_linear,
                  'period_nonlinear': periods_nonlin}).to_csv(
        os.path.join(OUTPUT_DIR['data'], 'period_vs_amplitude.csv'), index=False)

    print(f"  Linear model:   period range {np.nanmin(periods_linear):.4f} ~ {np.nanmax(periods_linear):.4f} s")
    print(f"  Nonlinear model: period range {np.nanmin(periods_nonlin):.4f} ~ {np.nanmax(periods_nonlin):.4f} s")
    if np.std(periods_linear) < 1e-6:
        print("  -> Linear model: isochronous (period independent of amplitude)")
    if np.std(periods_nonlin) > 1e-3:
        print("  -> Nonlinear model: non-isochronism observed")

    print("T3 done.\n")


def run_wave_propagation(params):
    """T4: 一维波动方程求解 — 高斯波包传播 + 两端固定边界"""
    print("=" * 50)
    print("T4: 1D Wave Equation Solver (Standing Wave)")
    print("=" * 50)

    L = params['L']
    G = params['G']
    rho = params['rho']
    nx = WAVE_SOLVER['nx']
    nt = WAVE_SOLVER['nt']
    CFL = WAVE_SOLVER['CFL']
    v = wave_speed(G, rho)

    print(f"  Rubber band length L = {L:.3f} m")
    print(f"  Shear modulus G = {G:.1e} Pa")
    print(f"  Density rho = {rho:.0f} kg/m^3")
    print(f"  Wave speed v = {v:.2f} m/s")
    print(f"  Fundamental freq f1 = {v/(2*L):.2f} Hz")

    # 两端固定边界 + 高斯波包初始条件
    print("\n>> Fixed-fixed boundary + Gaussian initial wave packet...")
    u, x, t, dt, dx = solve_wave_equation(
        L=L, G=G, rho=rho, nx=nx, nt=nt, CFL=CFL,
        bc_type='fixed', initial_condition='gaussian'
    )
    print(f"  Grid: nx={nx}, nt={nt}")
    print(f"  dt={dt:.6e}s, dx={dx:.6e}m, CFL={CFL}")

    # 能量守恒检查
    energy = compute_energy(u, dx, v)
    energy_drift = (energy[-1] - energy[0]) / energy[0]
    print(f"  Energy conservation: drift = {energy_drift:.4e}")

    # 生成时空图
    plot_spacetime(u, x, t,
                   save_path=os.path.join(OUTPUT_DIR['figures'], 'T4_spacetime.png'))

    # 生成初始和最终快照
    plot_snapshot(u, x, t, 0, label=f't={t[0]:.4f}s (initial)',
                  save_path=os.path.join(OUTPUT_DIR['figures'], 'T4_snapshot_initial.png'))
    plot_snapshot(u, x, t, min(nt-1, int(nt*0.8)),
                  label=f't={t[min(nt-1, int(nt*0.8))]:.4f}s',
                  save_path=os.path.join(OUTPUT_DIR['figures'], 'T4_snapshot_final.png'))

    # 驻波模式图
    plot_standing_wave_modes(u, x, t, n_modes=4,
                             save_path=os.path.join(OUTPUT_DIR['figures'], 'T4_standing_modes.png'))

    print("T4 done.\n")
    return u, x, t, dt, dx, v


def run_driven_analysis(params):
    """T5: 驱动端边界条件下的驻波分析"""
    print("=" * 50)
    print("T5: Driven Boundary - Standing Wave Mode Analysis")
    print("=" * 50)

    L = params['L']
    G = params['G']
    rho = params['rho']
    v = wave_speed(G, rho)
    f1 = v / (2 * L)

    print(f"  Fundamental frequency f1 = {f1:.2f} Hz")

    results = []
    modes_to_excite = [1, 2, 3, 4]
    all_nodes = []

    for mode_n in modes_to_excite:
        drive_freq = mode_n * f1
        print(f"\n>> Driving at f = {drive_freq:.2f} Hz (mode {mode_n})...")

        # 驱动端边界条件
        def excitation(t, freq=drive_freq):
            return 0.5 * np.sin(2 * np.pi * freq * t)

        # 需要足够多的时间步以形成稳态
        nt_driven = int(WAVE_SOLVER['nt'] * 2)
        u, x, t, dt, dx = solve_wave_equation(
            L=L, G=G, rho=rho, nx=WAVE_SOLVER['nx'], nt=nt_driven,
            CFL=WAVE_SOLVER['CFL'],
            bc_type='driven', excitation=excitation,
            initial_condition='zero'
        )

        # 时空图
        plot_spacetime(u, x, t,
                       save_path=os.path.join(OUTPUT_DIR['figures'],
                                              f'T5_mode{mode_n}_spacetime.png'))

        # 检测节点
        nodes = find_nodes(u, x, threshold=0.05)
        theory_nodes = theoretical_nodes(mode_n, L)
        err = node_error(nodes, theory_nodes)

        if nodes is not None and len(nodes) > 0:
            print(f"  Detected nodes: {np.round(nodes, 4)}")
        if theory_nodes is not None and len(theory_nodes) > 0:
            print(f"  Theoretical nodes: {np.round(theory_nodes, 4)}")
        if err:
            print(f"  Node error: mean={err['mean_error']:.4e}, max={err['max_error']:.4e}")

        results.append({
            'mode': mode_n,
            'frequency': drive_freq,
            'nodes_numerical': nodes,
            'nodes_theoretical': theory_nodes,
            'error': err,
        })
        all_nodes.append((f'Mode {mode_n} (num)', nodes))

    # 保存数据
    pd.DataFrame([{
        'mode': r['mode'],
        'frequency': r['frequency'],
        'node_count_numerical': len(r['nodes_numerical']) if r['nodes_numerical'] is not None else 0,
        'node_count_theoretical': len(r['nodes_theoretical']),
        'mean_error': r['error']['mean_error'] if r['error'] else None,
    } for r in results]).to_csv(
        os.path.join(OUTPUT_DIR['data'], 'driven_modes.csv'), index=False)

    print("\nT5 done.\n")
    return results, all_nodes


def main():
    np.random.seed(RANDOM_SEED)
    ensure_dirs()
    params = DEFAULT_PARAMS.copy()

    print("Standing Wave on Rubber Band -- Python Simulation")
    print(f"Seed: {RANDOM_SEED}, Params: {params}\n")

    # Round 1: 2-DOF model (T1-T3)
    I = run_baseline(params)
    scan_results = run_parameter_scan(params, I)
    run_nonlinear_analysis(params, I)

    # Round 2: Continuous wave model (T4-T5)
    wave_p = {**WAVE_PARAMS}
    u, x, t, dt, dx, v = run_wave_propagation(wave_p)
    results, all_nodes = run_driven_analysis(wave_p)

    print("=" * 50)
    print("All simulations complete!")
    print(f"Figures: {OUTPUT_DIR['figures']}")
    print(f"Data:    {OUTPUT_DIR['data']}")
    print("=" * 50)


if __name__ == '__main__':
    main()
