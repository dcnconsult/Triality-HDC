"""EDMD (very small) for Koopman spectral signature of limit cycles."""
import numpy as np

def edmd(X, Y, dict_fn=None):
    """X,Y: snapshots (features x samples). dict_fn maps state to lifted features."""
    if dict_fn is None:
        dict_fn = lambda S: np.vstack([S, np.abs(S), S**2])
    PhiX = dict_fn(X)
    PhiY = dict_fn(Y)
    G = PhiX @ PhiX.T / X.shape[1]
    A = PhiY @ PhiX.T / X.shape[1]
    # regularize
    reg = 1e-6*np.eye(G.shape[0])
    K = np.linalg.solve(G + reg, A).T
    # eigen-decomposition
    evals, evecs = np.linalg.eig(K)
    return evals, evecs, K
