"""Clifford torus embedding, bundle-by-scale, and a proxy 'tension' functional."""
import numpy as np

def clifford_torus(u, v):
    """Return (x1,x2,x3,x4) on the Clifford torus in S^3.
    u, v can be arrays (broadcasting supported).
    """
    u = np.asarray(u); v = np.asarray(v)
    c = 1/np.sqrt(2.0)
    return np.stack([c*np.cos(u), c*np.sin(u), c*np.cos(v), c*np.sin(v)], axis=-1)

def phi():
    return (1 + 5**0.5)/2

def ladder_indices(k0=0, n=10):
    """Return scale ladder s_k with step log(phi)."""
    step = np.log(phi())
    ks = np.arange(k0, k0+n)
    s = ks * step
    return ks, s

def metric_tension_proxy(s, kappa0=1.0):
    """A toy 'tension' functional increasing as |s| grows (proxy for curvature strength).
    In practice, tie this to a scale-dependent metric on the torus fiber.
    """
    s = np.asarray(s)
    return kappa0 * (1.0 + np.abs(s))
