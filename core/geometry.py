import numpy as np
def clifford_torus(u, v):
    u = np.asarray(u); v = np.asarray(v); c = 1/np.sqrt(2.0)
    return np.stack([c*np.cos(u), c*np.sin(u), c*np.cos(v), c*np.sin(v)], axis=-1)
def phi(): return (1 + 5**0.5)/2
def ladder_indices(k0=0, n=10):
    step = np.log(phi()); ks = np.arange(k0, k0+n); s = ks*step; return ks, s
def metric_tension_proxy(s, kappa0=1.0):
    s = np.asarray(s); return kappa0*(1.0 + np.abs(s))
