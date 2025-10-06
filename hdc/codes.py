import numpy as np
from .vsa import rand_hv, bind_xor, bind_conv, superpose, permute, normalize
def make_vocab(D=8192, seed=0):
    rng = np.random.default_rng(seed)
    T = rand_hv(D, seed=rng.integers(1<<31)); A = [rand_hv(D, seed=rng.integers(1<<31)) for _ in range(3)]
    F0 = rand_hv(D, seed=rng.integers(1<<31)); return dict(T=T, A=A, F0=F0)
def F_k(F0, k, shift=101): return permute(F0, k*shift)
def triad_code(Ai, Aj, Ak, bind='xor'):
    return normalize(bind_xor(bind_xor(Ai,Aj),Ak) if bind=='xor' else bind_conv(bind_conv(Ai,Aj),Ak))
def slice_code(T, Fk, bind='xor'):
    return normalize(bind_xor(T, Fk) if bind=='xor' else bind_conv(T, Fk))
def state_code(triads, slice_vec, weights=None, bind='xor'):
    vecs = [ ( (lambda x,y: bind_xor(x,y) if bind=='xor' else bind_conv(x,y)) )(tri, slice_vec) for tri in triads ]
    return normalize(superpose(vecs, weights=weights))
