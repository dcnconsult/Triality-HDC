# Triality v2.0 – Reference Implementation (Scaffold)

This repository operationalizes the Triality framework with a **torus-bundled phase space**, **tri-linear closure**, **φ-scaled resonance ladder**, **hypergraph limit-cycle model**, and **Hyperdimensional Computing (HDC)** encodings.

## Quick Start

### **Cross-Platform Setup**
```bash
# Automatic setup (detects OS and configures environment)
./setup.sh                      # Unix/Linux/macOS
# OR
.\setup.ps1                     # Windows PowerShell
# OR
.\setup.bat                     # Windows Batch (if available)
```

### **Manual Setup**
```bash
# Create virtual environment
python -m venv .venv
# Activate (choose your platform):
source .venv/bin/activate       # Unix/Linux/macOS
# OR
.venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt
```

### **Run Complete Pipeline**
```bash
# Cross-platform options:
./run_full_pipeline.sh          # Unix/Linux/macOS
.\run_full_pipeline.bat         # Windows Batch
.\run_full_pipeline.ps1         # Windows PowerShell
make full                       # Makefile (Unix/Linux)
```

### **Run Individual Components**
```bash
# Basic experiments
python run_experiments.py

# Metrics only
./run_metrics.sh                # Unix/Linux/macOS
.\run_metrics.bat               # Windows Batch
.\run_metrics.ps1               # Windows PowerShell
make all                        # Makefile

# Individual experiments
python -m experiments.triad_sweep_phi
python -m experiments.hypergraph_limit
python -m experiments.retuning_latency

# Individual metrics
python -m experiments.phi_vs_rational_metrics
python -m experiments.koopman_gap_metrics
python -m experiments.latency_fit_metrics

# Ablations and aggregation
python -m experiments.ablations
python -m scripts.aggregate
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

## Complete Pipeline

The project includes a comprehensive pipeline for paper generation:

### **Core Metrics**
- **`phi_vs_rational_metrics.py`**: Bicoherence analysis comparing φ-scaled vs rational frequency ratios
- **`koopman_gap_metrics.py`**: Koopman eigenvalue analysis for hypergraph limit cycles  
- **`latency_fit_metrics.py`**: Retuning latency vs ladder distance analysis

### **Ablation Studies**
- **`ablations.py`**: Three key ablation studies:
  - **No triads (J=0)**: Kills R₃ and collapses Koopman gap
  - **φ vs convergents**: Tests 8/5, 13/8, 21/13 ratios vs φ
  - **Noise stress**: Quantifies gap/R₃ degradation vs noise level

### **Aggregation**
- **`scripts/aggregate.py`**: Generates CSV tables and summary report
  - Outputs: `results/*.csv` files for paper tables
  - Creates: `results/summary_report.md` with overview

### **Paper Integration**
- **Enhanced PDF**: Automatically generated with professional layout
- **Figures**: Automatically copied to `paper/figures/` for LaTeX
- **Tables**: CSV files ready for paper tables
- **Metrics**: JSON files for quantitative results
- **Complete Paper**: 8-page publication-ready PDF with all sections

## Cross-Platform Compatibility

### **Supported Operating Systems**
- ✅ **Windows** (10/11) - PowerShell, Batch, WSL
- ✅ **Linux** (Ubuntu, Debian, CentOS, etc.) - Bash, Make
- ✅ **macOS** (10.15+) - Bash, Make
- ✅ **WSL** (Windows Subsystem for Linux)

### **Scripts Available**
| Platform | Setup | Full Pipeline | Metrics Only |
|----------|-------|---------------|--------------|
| **Windows** | `.\setup.ps1` | `.\run_full_pipeline.bat` | `.\run_metrics.bat` |
| **PowerShell** | `.\setup.ps1` | `.\run_full_pipeline.ps1` | `.\run_metrics.ps1` |
| **Unix/Linux** | `./setup.sh` | `./run_full_pipeline.sh` | `./run_metrics.sh` |
| **Makefile** | Manual | `make full` | `make all` |

### **Requirements**
- **Python**: 3.10+ (tested on 3.10, 3.11, 3.12)
- **Dependencies**: See `requirements.txt`
- **Memory**: 4GB+ RAM recommended
- **Disk**: 1GB+ free space

## Notes
- This scaffold is **minimal but runnable**. It favors clarity over performance.
- Biological claims are treated as **modular hypotheses**; all code targets physics/engineering observables first.
- **Module Structure**: All directories (`core/`, `signals/`, `hdc/`, `hypergraph/`) are proper Python packages with `__init__.py` files.
- **Cross-Platform**: All scripts work on Windows, Linux, and macOS.
- **JSON Outputs**: Metrics are saved as JSON files for easy integration with LaTeX paper.
- **LaTeX Integration**: Figures automatically copied to `paper/figures/` for compilation.
- **Compatibility Testing**: Run `python test_cross_platform.py` to validate your setup.
- Licensed under Apache-2.0 (adjust as needed).

## Additional Documentation
- **[Cross-Platform Summary](CROSS_PLATFORM_SUMMARY.md)**: Complete compatibility guide
- **[Paper Completion Guide](PAPER_COMPLETION_GUIDE.md)**: Step-by-step paper generation
