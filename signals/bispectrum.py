import numpy as np
from numpy.fft import rfft
def _stft(x, nperseg, noverlap):
    step = nperseg - noverlap; n = len(x); segments = []
    for start in range(0, n - nperseg + 1, step):
        seg = x[start:start+nperseg]*np.hanning(nperseg); segments.append(rfft(seg))
    return np.array(segments).T
def bicoherence(x, y, z, nperseg=1024, noverlap=512):
    X = _stft(x, nperseg, noverlap); Y = _stft(y, nperseg, noverlap); Z = _stft(z, nperseg, noverlap)
    F = X.shape[0]; B = np.zeros((F, F), dtype=complex); Pxyz = np.zeros((F, F))
    PX = np.mean(np.abs(X)**2, axis=1); PY = np.mean(np.abs(Y)**2, axis=1); PZ = np.mean(np.abs(Z)**2, axis=1)
    for f1 in range(F):
        for f2 in range(F - f1):
            prod = X[f1]*Y[f2]*np.conj(Z[f1+f2]); B[f1,f2] = np.mean(prod)
            denom = PX[f1]*PY[f2]*PZ[f1+f2] + 1e-12; Pxyz[f1,f2] = np.abs(B[f1,f2])**2/denom
    return B, Pxyz
