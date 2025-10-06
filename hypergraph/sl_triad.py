"""Stuart–Landau hypergraph with triadic couplings."""
import numpy as np
from scipy.integrate import solve_ivp

def sl_triad_rhs(t, y, N, edges3, alpha=0.2, J=0.1, noise=0.0, rng=None):
    z = y[:N] + 1j*y[N:]
    dz = (alpha - np.abs(z)**2)*z
    for i,j,k in edges3:
        dz[i] += J * z[j]*z[k]
        dz[j] += J * z[i]*z[k]
        dz[k] += J * z[i]*z[j]
    if noise and rng is not None:
        dz += noise*(rng.standard_normal(N)+1j*rng.standard_normal(N))
    return np.concatenate([dz.real, dz.imag])

def simulate_sl(N=200, m_edges=300, alpha=0.2, J=0.08, T=200, max_step=0.2, seed=0):
    rng = np.random.default_rng(seed)
    # random 3-edges
    edges3 = [tuple(rng.choice(N, size=3, replace=False)) for _ in range(m_edges)]
    y0c = 0.1*(rng.standard_normal(N)+1j*rng.standard_normal(N))
    y0 = np.concatenate([y0c.real, y0c.imag])
    sol = solve_ivp(lambda t,y: sl_triad_rhs(t,y,N,edges3,alpha,J,0.0,rng), (0,T), y0, max_step=max_step)
    z = sol.y[:N] + 1j*sol.y[N:]
    return sol.t, z, edges3

def order_params(z):
    phi = np.angle(z)
    R2 = np.abs(np.mean(np.exp(1j*phi)))
    # crude R3: sample random triads
    N = z.shape[0]
    rng = np.random.default_rng(0)
    triads = [tuple(rng.choice(N,3,replace=False)) for _ in range(min(2000, N))]
    vals = []
    for i,j,k in triads:
        vals.append(np.exp(1j*(phi[i]+phi[j]+phi[k])))
    R3 = np.abs(np.mean(vals))
    return R2, R3
