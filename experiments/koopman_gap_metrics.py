import json, numpy as np, matplotlib.pyplot as plt
from hypergraph.sl_triad import simulate_sl, order_params
from hypergraph.koopman import edmd
from signals.analysis_metrics import spectral_gap
def main():
    t, z, edges3 = simulate_sl(N=400, m_edges=600, J=0.10, T=300)
    R2, R3 = order_params(z[:,-1]); X = z[:, :-1].real; Y = z[:, 1:  ].real
    evals, evecs, K = edmd(X, Y, dict_fn=lambda S: np.vstack([S, S**2]))
    lead, second, gap = spectral_gap(evals)
    out = dict(R2=float(R2), R3=float(R3), lead=float(lead), second=float(second), gap=float(gap))
    with open("results/koopman_summary.json", "w") as f: json.dump(out, f, indent=2)
    plt.figure(); plt.hist(np.abs(evals), bins=40); plt.title('Koopman eigenvalue magnitudes')
    plt.savefig('results/koopman_hist.png', dpi=160)
if __name__ == "__main__": main()
