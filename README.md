# Triality v2.0 – Reference Implementation (Scaffold)

This repository operationalizes the Triality framework with a **torus-bundled phase space**, **tri-linear closure**, **φ-scaled resonance ladder**, **hypergraph limit-cycle model**, and **Hyperdimensional Computing (HDC)** encodings.

## Quick Start
```bash
# (Recommended) Python 3.10+
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run all experiments (recommended)
python run_experiments.py

# Run metrics pipeline (generates JSON outputs for paper)
python run_metrics.ps1          # PowerShell (Windows)
# OR
run_metrics.bat                 # Batch script (Windows)
# OR
make all                        # Makefile (Unix/Linux)

# Or run individual experiments as modules:
python -m experiments.triad_sweep_phi
python -m experiments.hypergraph_limit
python -m experiments.retuning_latency

# Individual metrics experiments:
python -m experiments.phi_vs_rational_metrics
python -m experiments.koopman_gap_metrics
python -m experiments.latency_fit_metrics
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

## Metrics System
The project includes a comprehensive metrics pipeline that generates quantitative results for the paper:

- **`phi_vs_rational_metrics.py`**: Bicoherence analysis comparing φ-scaled vs rational frequency ratios
  - Outputs: `results/bic_phi.json`, `results/bic_rational.json`
  - Metrics: peak bicoherence, area above threshold, compactness

- **`koopman_gap_metrics.py`**: Koopman eigenvalue analysis for hypergraph limit cycles
  - Outputs: `results/koopman_summary.json`
  - Metrics: leading eigenvalue magnitude, spectral gap

- **`latency_fit_metrics.py`**: Retuning latency vs ladder distance analysis
  - Outputs: `results/latency_fit.json`
  - Metrics: linear fit slope, intercept, R²

## Notes
- This scaffold is **minimal but runnable**. It favors clarity over performance.
- Biological claims are treated as **modular hypotheses**; all code targets physics/engineering observables first.
- **Module Structure**: All directories (`core/`, `signals/`, `hdc/`, `hypergraph/`) are proper Python packages with `__init__.py` files.
- **Running Scripts**: Use `python -m module.name` syntax or the convenience scripts.
- **JSON Outputs**: Metrics are saved as JSON files for easy integration with LaTeX paper.
- Licensed under Apache-2.0 (adjust as needed).
