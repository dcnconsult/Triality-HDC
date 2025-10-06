import numpy as np
from .vsa import cos_sim, normalize
class HDMemory:
    def __init__(self, D=8192):
        self.D = D; self.keys = []; self.values = []
    def add(self, key, value):
        self.keys.append(normalize(key)); self.values.append(normalize(value))
    def query(self, key, topk=1):
        key = normalize(key); sims = [cos_sim(key, k) for k in self.keys]
        idx = np.argsort(sims)[::-1][:topk]; return [(int(i), float(sims[i]), self.values[i]) for i in idx]
    def hebbian_update(self, key, value, eta=0.1):
        if not self.keys: self.add(key, value); return
        idx, _, _ = self.query(key, topk=1)[0]
        self.keys[idx] = normalize(self.keys[idx] + eta*key); self.values[idx] = normalize(self.values[idx] + eta*value)
