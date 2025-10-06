"""Encodings for scales (F_k), angles/modes (A_i), torus (T), and slice S_k."""
import numpy as np
from .vsa import rand_hv, bind_xor, bind_conv, superpose, permute, normalize

def make_vocab(D=8192, seed=0):
    rng = np.random.default_rng(seed)
    T = rand_hv(D, seed=rng.integers(1<<31))
    A = [rand_hv(D, seed=rng.integers(1<<31)) for _ in range(3)]
    F0 = rand_hv(D, seed=rng.integers(1<<31))
    return dict(T=T, A=A, F0=F0)

def F_k(F0, k, shift=101):
    return permute(F0, k*shift)

def triad_code(Ai, Aj, Ak, bind='xor'):
    if bind=='xor':
        return normalize(bind_xor(bind_xor(Ai,Aj),Ak))
    else:
        return normalize(bind_conv(bind_conv(Ai,Aj),Ak))

def slice_code(T, Fk, bind='xor'):
    if bind=='xor':
        return normalize(bind_xor(T, Fk))
    else:
        return normalize(bind_conv(T, Fk))

def state_code(triads, slice_vec, weights=None, bind='xor'):
    vecs = []
    for tri in triads:
        if bind=='xor':
            vecs.append(bind_xor(tri, slice_vec))
        else:
            vecs.append(bind_conv(tri, slice_vec))
    return normalize(superpose(vecs, weights=weights))
