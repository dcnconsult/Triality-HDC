import numpy as np
PHI = (1 + 5**0.5)/2
def step_log_phi(): return np.log(PHI)
def freq_ladder(f0, k:int): return f0*(PHI**k)
def scale_ladder(s0, k:int): return s0 + k*step_log_phi()
