import numpy as np
import matplotlib.pyplot as plt
from core.triad_hamiltonian import simulate_triad, analytic_signal
from core.transitions import retuning_latency

def run_latency(kappa=0.03, wc=2.2, sweep=6):
    PHI = (1+5**0.5)/2
    res = []
    for dk in range(-sweep, sweep+1):
        wb = PHI**(1+dk*0.1) # move along a small fraction of the ladder per step
        t, Y = simulate_triad(wa=1.0, wb=wb, wc=wc, kappa=kappa, tspan=(0,400))
        a,b,c = analytic_signal(Y)
        lat = retuning_latency(t, a,b,c)
        res.append((dk, lat))
        print(f"Δk={dk:2d}  latency={lat}")
    return np.array(res)

def main():
    res = run_latency()
    plt.figure()
    plt.plot(res[:,0], res[:,1], 'o-')
    plt.xlabel('Δk (ladder steps, fractional)')
    plt.ylabel('retuning latency (a.u.)')
    plt.title('Latency vs ladder distance')
    plt.savefig('results/latency_vs_ladder.png', dpi=160)

if __name__=='__main__':
    main()
