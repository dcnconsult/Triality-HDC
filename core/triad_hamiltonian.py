import numpy as np
from scipy.integrate import solve_ivp
def triad_rhs(t, y, wa, wb, wc, kappa):
    a = y[0] + 1j*y[1]; b = y[2] + 1j*y[3]; c = y[4] + 1j*y[5]
    da = -1j*wa*a -1j*kappa*np.conj(b)*np.conj(c)
    db = -1j*wb*b -1j*kappa*np.conj(a)*np.conj(c)
    dc = -1j*wc*c -1j*kappa*np.conj(a)*np.conj(b)
    return np.array([da.real, da.imag, db.real, db.imag, dc.real, dc.imag], dtype=float)
def simulate_triad(tspan=(0, 200), y0=None, wa=1.0, wb=1.618, wc=2.618, kappa=0.02, max_step=0.1):
    if y0 is None:
        rng = np.random.default_rng(0)
        y0c = (rng.standard_normal(3) + 1j*rng.standard_normal(3))*0.1
        y0 = np.array([y0c[0].real,y0c[0].imag,y0c[1].real,y0c[1].imag,y0c[2].real,y0c[2].imag])
    sol = solve_ivp(lambda t,y: triad_rhs(t,y,wa,wb,wc,kappa), tspan, y0, max_step=max_step, dense_output=False)
    return sol.t, sol.y.reshape(6,-1)
def analytic_signal(y):
    a = y[0] + 1j*y[1]; b = y[2] + 1j*y[3]; c = y[4] + 1j*y[5]; return a,b,c
