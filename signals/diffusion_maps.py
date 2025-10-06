"""Tiny diffusion maps for latent toroidal coordinate recovery."""
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

def diffusion_maps(X, epsilon=None, n_components=3):
    D2 = pairwise_distances(X, metric='sqeuclidean')
    if epsilon is None:
        # median heuristic
        eps = np.median(D2[D2>0])
    else:
        eps = epsilon
    K = np.exp(-D2/(eps+1e-12))
    d = K.sum(axis=1, keepdims=True)
    A = K/(d+1e-12)
    w, v = np.linalg.eig(A.T)
    idx = np.argsort(-np.abs(w))
    return w[idx][:n_components], v[:,idx][:,:n_components]
