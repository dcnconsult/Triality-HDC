import numpy as np, matplotlib.pyplot as plt
from core.triad_hamiltonian import simulate_triad, analytic_signal
from signals.bispectrum import bicoherence

def run_case(wb, wc, tag):
    t, Y = simulate_triad(wa=1.0, wb=wb, wc=wc, kappa=0.03, tspan=(0,400))
    a,b,c = analytic_signal(Y); x,y,z = a.real, b.real, c.real
    B, bic = bicoherence(x,y,z, nperseg=512, noverlap=256)
    vmax = np.nanmax(bic); print(f"{tag}: max bicoherence = {vmax:.3f}")
    plt.figure(); plt.imshow(bic.T, origin='lower', aspect='auto'); plt.title(f'Bicoherence map: {tag}')
    plt.xlabel('f1 index'); plt.ylabel('f2 index'); plt.colorbar(label='bicoherence')
    plt.savefig('results/bicoherence_'+tag+'.png', dpi=160)

def main():
    PHI = (1+5**0.5)/2
    run_case(wb=PHI, wc=1+PHI, tag='phi')
    run_case(wb=1.5, wc=1.6666667, tag='rational')

if __name__=='__main__': main()
