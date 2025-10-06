import os, json, glob, pandas as pd
def load_json(fp):
    with open(fp) as f: return json.load(f)
def main():
    os.makedirs("results", exist_ok=True)
    tables = {}
    # Bicoherence
    paths = [p for p in glob.glob("results/bic_*.json")]
    rows = []
    for p in paths:
        tag = os.path.basename(p).split("bic_")[-1].split(".json")[0]
        obj = load_json(p); obj["case"]=tag; rows.append(obj)
    if rows: 
        df = pd.DataFrame(rows); tables["bicoherence_summary"]=df
    # Koopman
    p = "results/koopman_summary.json"
    if os.path.exists(p): tables["koopman_summary"] = pd.DataFrame([load_json(p)])
    # Latency fit (optional future)
    p = "results/latency_fit.json"
    if os.path.exists(p): tables["latency_fit"] = pd.DataFrame([load_json(p)])
    # Ablations
    p = "results/abl_no_triads.json"
    if os.path.exists(p): tables["ablation_no_triads"] = pd.DataFrame([load_json(p)])
    p = "results/abl_phi_convergents.json"
    if os.path.exists(p):
        obj = load_json(p); rows = [dict(case=k, **v) for k,v in obj.items()]
        tables["ablation_phi_convergents"] = pd.DataFrame(rows)
    p = "results/abl_noise_stress.json"
    if os.path.exists(p):
        obj = load_json(p); tables["ablation_noise"] = pd.DataFrame(obj)
    for name, df in tables.items():
        df.to_csv(f"results/{name}.csv", index=False)
    with open("results/summary_report.md","w") as f:
        f.write("# Summary tables\n" + "\n".join(f"- {k}" for k in tables.keys()))
    print("Wrote tables:", list(tables.keys()))
if __name__ == "__main__":
    main()
