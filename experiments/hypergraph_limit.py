import numpy as np, matplotlib.pyplot as plt
from hypergraph.sl_triad import simulate_sl, order_params
from hypergraph.koopman import edmd
def main():
    t, z, edges3 = simulate_sl(N=400, m_edges=600, J=0.10, T=300)
    R2, R3 = order_params(z[:,-1]); print(f"R2={R2:.3f}, R3={R3:.3f}")
    X = z[:, :-1].real; Y = z[:, 1:  ].real
    evals, evecs, K = edmd(X, Y, dict_fn=lambda S: np.vstack([S, S**2]))
    idx = np.argsort(-np.abs(evals)); dom = evals[idx[0]]; print(f"Leading Koopman |λ|={np.abs(dom):.4f}")
    plt.figure(); plt.hist(np.abs(evals), bins=40); plt.title('Koopman eigenvalue magnitudes')
    plt.savefig('results/koopman_hist.png', dpi=160)
if __name__=='__main__': main()
