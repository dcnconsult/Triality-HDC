# Triality v2.0 – Reference Implementation (Scaffold)

This repository operationalizes the Triality framework with a **torus-bundled phase space**, **tri-linear closure**, **φ-scaled resonance ladder**, **hypergraph limit-cycle model**, and **Hyperdimensional Computing (HDC)** encodings.

## Quick Start
```bash
# (Recommended) Python 3.10+
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run a φ-step triad sweep simulation and compute bicoherence
python experiments/triad_sweep_phi.py

# Toggle triadic hypergraph couplings and analyze Koopman spectrum
python experiments/hypergraph_limit.py

# Explore retuning latency vs ladder distance
python experiments/retuning_latency.py
```

## Layout
```
triality/
  core/                # geometry, φ-ladder, triad Hamiltonian, transitions
  hypergraph/          # Stuart–Landau triadic network, Koopman analysis
  signals/             # bispectrum/bicoherence, diffusion maps, TDA
  hdc/                 # VSA encodings for triads × scale × geometry
  experiments/         # runnable scripts reproducing paper figures
  data/                # datasets (drop-in)
  results/             # generated figures/tables
  paper/               # preprint.tex and figures
```

## Notes
- This scaffold is **minimal but runnable**. It favors clarity over performance.
- Biological claims are treated as **modular hypotheses**; all code targets physics/engineering observables first.
- Licensed under Apache-2.0 (adjust as needed).
