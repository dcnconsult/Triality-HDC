import numpy as np
def bicoherence_metrics(bic, top_p=0.01, thresh=None):
    B = np.asarray(bic); peak = float(np.nanmax(B))
    flat = B.flatten(); flat = flat[~np.isnan(flat)]
    if thresh is None: thresh = float(np.quantile(flat, 0.99)) if len(flat) else 1.0
    area_above = float((B >= thresh).sum()) / float(B.size if B.size else 1)
    k = max(1, int(len(flat) * top_p)); topk_mean = float(np.mean(np.sort(flat)[-k:])) if len(flat) else 1.0
    compactness = peak / (topk_mean + 1e-12)
    return dict(peak=peak, area_above=area_above, compactness=compactness, thresh=thresh)
def spectral_gap(eigs):
    vals = np.abs(np.asarray(eigs)); 
    if vals.size == 0: return np.nan, np.nan, np.nan
    idx = np.argsort(-vals)
    if len(idx) < 2: return float(vals[idx[0]]), np.nan, np.nan
    lead = float(vals[idx[0]]); second = float(vals[idx[1]]); gap = lead - second; return lead, second, gap
def linear_fit(x, y):
    x = np.asarray(x).ravel(); y = np.asarray(y).ravel()
    m = np.isfinite(x) & np.isfinite(y); x = x[m]; y = y[m]
    if len(x) < 2: return dict(slope=np.nan, intercept=np.nan, r2=np.nan)
    X = np.vstack([x, np.ones_like(x)]).T
    beta, *_ = np.linalg.lstsq(X, y, rcond=None); yhat = X @ beta
    ss_res = float(np.sum((y - yhat)**2)); ss_tot = float(np.sum((y - np.mean(y))**2) + 1e-12)
    r2 = 1 - ss_res/ss_tot; return dict(slope=float(beta[0]), intercept=float(beta[1]), r2=float(r2))
