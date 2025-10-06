"""Minimal VSA/HDC: binary and real hypervectors, binding via XOR or circular convolution."""
import numpy as np

def rand_hv(D=10000, bipolar=True, seed=None):
    rng = np.random.default_rng(seed)
    if bipolar:
        return rng.choice([-1,1], size=D).astype(float)
    return rng.standard_normal(D)

def bind_xor(a,b):
    return a*b  # bipolar: XOR == elementwise product

def bind_conv(a,b):
    # circular convolution via FFT
    A = np.fft.rfft(a); B = np.fft.rfft(b)
    C = A*B
    return np.fft.irfft(C, n=len(a))

def superpose(vecs, weights=None):
    V = np.array(vecs)
    if weights is None:
        return V.mean(axis=0)
    w = np.asarray(weights).reshape(-1,1)
    return (V*w).sum(axis=0)

def normalize(a):
    return a/ (np.linalg.norm(a)+1e-12)

def permute(a, shift):
    return np.roll(a, shift)

def cos_sim(a,b):
    return float(np.dot(a,b)/((np.linalg.norm(a)+1e-12)*(np.linalg.norm(b)+1e-12)))
