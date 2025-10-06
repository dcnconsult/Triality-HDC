import json, numpy as np, matplotlib.pyplot as plt
from core.triad_hamiltonian import simulate_triad, analytic_signal
from signals.bispectrum import bicoherence
from signals.analysis_metrics import bicoherence_metrics
def run(wb, wc, tag):
    t, Y = simulate_triad(wa=1.0, wb=wb, wc=wc, kappa=0.03, tspan=(0, 400))
    a,b,c = analytic_signal(Y); B, bic = bicoherence(a.real, b.real, c.real, nperseg=512, noverlap=256)
    m = bicoherence_metrics(bic); np.savez(f"results/bic_{tag}.npz", bic=bic, metrics=m)
    with open(f"results/bic_{tag}.json", "w") as fh: json.dump(m, fh, indent=2)
    plt.figure(); plt.imshow(bic.T, origin='lower', aspect='auto'); plt.title(f"Bicoherence: {tag}"); plt.colorbar()
    plt.savefig(f"results/bico_{tag}.png", dpi=160)
def main():
    PHI = (1 + 5**0.5)/2; run(PHI, 1.0 + PHI, "phi"); run(1.5, 1.6666667, "rational")
    print(open("results/bic_phi.json").read()); print(open("results/bic_rational.json").read())
if __name__ == "__main__": main()
