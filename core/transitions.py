import numpy as np
def retuning_latency(time, a,b,c):
    dom = np.array([np.argmax([abs(a[i])**2, abs(b[i])**2, abs(c[i])**2]) for i in range(len(time))])
    changes = np.where(np.diff(dom)!=0)[0]
    if len(changes)<1: return np.nan
    return float(np.mean(np.diff(time[changes])))
