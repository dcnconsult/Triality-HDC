import numpy as np
def dominant_mode(a,b,c):
    e = np.array([np.mean(np.abs(a)**2), np.mean(np.abs(b)**2), np.mean(np.abs(c)**2)])
    return int(np.argmax(e)), e
def retuning_latency(time, a,b,c):
    dom = np.array([np.argmax([abs(a[i])**2, abs(b[i])**2, abs(c[i])**2]) for i in range(len(time))])
    changes = np.where(np.diff(dom)!=0)[0]
    if len(changes)<1: return np.nan
    return float(np.mean(np.diff(time[changes])))
