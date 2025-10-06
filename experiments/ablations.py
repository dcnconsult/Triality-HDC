import json, numpy as np
from hypergraph.sl_triad import simulate_sl, order_params
from hypergraph.koopman import edmd
from core.triad_hamiltonian import simulate_triad, analytic_signal
from signals.bispectrum import bicoherence
from signals.analysis_metrics import bicoherence_metrics, spectral_gap

def hypergraph_no_triads(N=400, T=300):
    from scipy.integrate import solve_ivp
    alpha=0.2
    def rhs(t, y):
        z = y[:N] + 1j*y[N:]
        dz = (alpha - np.abs(z)**2)*z
        return np.concatenate([dz.real, dz.imag])
    import numpy as np
    rng = np.random.default_rng(0)
    y0c = 0.1*(rng.standard_normal(N)+1j*rng.standard_normal(N))
    y0 = np.concatenate([y0c.real, y0c.imag])
    sol = solve_ivp(rhs, (0,T), y0, max_step=0.2)
    z = sol.y[:N] + 1j*sol.y[N:]
    X = z[:, :-1].real; Y = z[:, 1:].real
    evals, evecs, K = edmd(X, Y, dict_fn=lambda S: np.vstack([S, S**2]))
    lead, second, gap = spectral_gap(evals)
    R2, R3 = order_params(z[:,-1])
    return dict(lead=float(lead), second=float(second), gap=float(gap), R2=float(R2), R3=float(R3))

def phi_vs_convergents():
    PHI = (1+5**0.5)/2
    cases = {
        "phi": (PHI, 1.0+PHI),
        "8_5": (8/5, 13/8),
        "13_8": (13/8, 21/13),
        "21_13": (21/13, 34/21)
    }
    out = {}
    for tag, (wb, wc) in cases.items():
        t, Y = simulate_triad(wa=1.0, wb=wb, wc=wc, kappa=0.03, tspan=(0, 400))
        a,b,c = analytic_signal(Y)
        _, bic = bicoherence(a.real, b.real, c.real, nperseg=512, noverlap=256)
        m = bicoherence_metrics(bic)
        out[tag] = m
    return out

def noise_stress(levels=(0.0, 0.02, 0.05, 0.1)):
    res = []
    t, z, edges3 = simulate_sl(N=300, m_edges=450, J=0.10, T=240)
    from numpy.random import default_rng
    rng = default_rng(0)
    for noise in levels:
        X = z[:, :-1].real + noise*rng.standard_normal(z[:, :-1].shape)
        Y = z[:, 1:  ].real + noise*rng.standard_normal(z[:, 1:  ].shape)
        evals, evecs, K = edmd(X, Y, dict_fn=lambda S: np.vstack([S, S**2]))
        lead, second, gap = spectral_gap(evals)
        R2, R3 = order_params(z[:,-1])
        res.append(dict(noise=noise, lead=float(lead), second=float(second), gap=float(gap), R2=float(R2), R3=float(R3)))
    return res

def main():
    with open("results/abl_no_triads.json","w") as f: json.dump(hypergraph_no_triads(), f, indent=2)
    with open("results/abl_phi_convergents.json","w") as f: json.dump(phi_vs_convergents(), f, indent=2)
    with open("results/abl_noise_stress.json","w") as f: json.dump(noise_stress(), f, indent=2)
    print("Ablations written to results/")

if __name__ == "__main__":
    main()
