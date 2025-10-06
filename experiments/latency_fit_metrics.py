import json, numpy as np, matplotlib.pyplot as plt
from core.triad_hamiltonian import simulate_triad, analytic_signal
from core.transitions import retuning_latency
from signals.analysis_metrics import linear_fit
def run_latency(kappa=0.03, wc=2.2, sweep=8):
    PHI = (1+5**0.5)/2; res = []
    for dk in range(-sweep, sweep+1):
        wb = PHI**(1+dk*0.12)
        t, Y = simulate_triad(wa=1.0, wb=wb, wc=wc, kappa=kappa, tspan=(0,450))
        a,b,c = analytic_signal(Y); lat = retuning_latency(t, a,b,c); res.append((dk, lat))
    return np.array(res, dtype=float)
def main():
    res = run_latency(); x = np.abs(res[:,0]); y = res[:,1]; fit = linear_fit(x, y)
    with open("results/latency_fit.json", "w") as f: json.dump(dict(points=res.tolist(), **fit), f, indent=2)
    plt.figure(); plt.plot(res[:,0], y, 'o'); xx = np.linspace(min(res[:,0]), max(res[:,0]), 200)
    plt.plot(xx, fit['slope']*np.abs(xx)+fit['intercept'], '-'); plt.xlabel('Δk (|steps|)'); plt.ylabel('latency')
    plt.title(f"Latency vs ladder distance (R^2={fit['r2']:.3f})"); plt.savefig("results/latency_fit.png", dpi=160); print(fit)
if __name__ == "__main__": main()
