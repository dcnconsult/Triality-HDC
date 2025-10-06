import numpy as np
def edmd(X, Y, dict_fn=None):
    if dict_fn is None:
        dict_fn = lambda S: np.vstack([S, np.abs(S), S**2])
    PhiX = dict_fn(X); PhiY = dict_fn(Y)
    G = PhiX @ PhiX.T / max(1, X.shape[1]); A = PhiY @ PhiX.T / max(1, X.shape[1])
    reg = 1e-6*np.eye(G.shape[0]); K = np.linalg.solve(G + reg, A).T
    evals, evecs = np.linalg.eig(K); return evals, evecs, K
