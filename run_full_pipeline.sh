#!/bin/bash
# Linux/Unix shell script for complete Triality pipeline
# Equivalent to: make full

echo "Triality v2.0 - Full Pipeline Execution"
echo "======================================="

# Ensure results directory exists
mkdir -p results

echo ""
echo "[1/5] Running core metrics..."

echo "  Running phi_vs_rational_metrics..."
python -m experiments.phi_vs_rational_metrics
if [ $? -ne 0 ]; then
    echo "ERROR: phi_vs_rational_metrics failed"
    exit 1
fi
echo "  ✓ phi_vs_rational_metrics completed"

echo "  Running koopman_gap_metrics..."
python -m experiments.koopman_gap_metrics
if [ $? -ne 0 ]; then
    echo "ERROR: koopman_gap_metrics failed"
    exit 1
fi
echo "  ✓ koopman_gap_metrics completed"

echo "  Running latency_fit_metrics..."
python -m experiments.latency_fit_metrics
if [ $? -ne 0 ]; then
    echo "ERROR: latency_fit_metrics failed"
    exit 1
fi
echo "  ✓ latency_fit_metrics completed"

echo ""
echo "[2/5] Running ablations..."
python -m experiments.ablations
if [ $? -ne 0 ]; then
    echo "ERROR: ablations failed"
    exit 1
fi
echo "✓ ablations completed"

echo ""
echo "[3/5] Running aggregation..."
python -m scripts.aggregate
if [ $? -ne 0 ]; then
    echo "ERROR: aggregation failed"
    exit 1
fi
echo "✓ aggregation completed"

echo ""
echo "[4/5] Copying figures to paper/figures/..."

# Copy figures to paper directory
if [ -f "results/bico_phi.png" ]; then
    cp "results/bico_phi.png" "paper/figures/bico_phi_placeholder.png"
    echo "  ✓ Copied bico_phi.png"
else
    echo "  ⚠ Warning: bico_phi.png not found"
fi

if [ -f "results/bico_rational.png" ]; then
    cp "results/bico_rational.png" "paper/figures/bico_rational_placeholder.png"
    echo "  ✓ Copied bico_rational.png"
else
    echo "  ⚠ Warning: bico_rational.png not found"
fi

if [ -f "results/koopman_hist.png" ]; then
    cp "results/koopman_hist.png" "paper/figures/koop_hist_placeholder.png"
    echo "  ✓ Copied koopman_hist.png"
else
    echo "  ⚠ Warning: koopman_hist.png not found"
fi

if [ -f "results/latency_fit.png" ]; then
    cp "results/latency_fit.png" "paper/figures/latency_placeholder.png"
    echo "  ✓ Copied latency_fit.png"
else
    echo "  ⚠ Warning: latency_fit.png not found"
fi

echo ""
echo "[5/5] Generating summary report..."

# Generate summary report
cat > "results/pipeline_summary.md" << 'EOF'
# Triality v2.0 - Pipeline Results Summary

## Generated Files

### JSON Metrics
- bic_phi.json, bic_rational.json - Bicoherence metrics
- koopman_summary.json - Koopman eigenvalue analysis
- latency_fit.json - Retuning latency fit parameters

### Ablation Studies
- abl_no_triads.json - No triads (J=0) analysis
- abl_phi_convergents.json - φ vs convergents comparison
- abl_noise_stress.json - Noise stress test results

### CSV Tables
- bicoherence_summary.csv - Bicoherence comparison table
- koopman_summary.csv - Koopman metrics table
- latency_fit.csv - Latency fit parameters
- ablation_*.csv - Ablation study tables

### Figures
- bico_phi.png, bico_rational.png - Bicoherence plots
- koopman_hist.png - Koopman eigenvalue histogram
- latency_fit.png - Latency vs ladder distance fit

## Next Steps
1. Review generated figures in paper/figures/
2. Compile preprint.tex with updated figures
3. Use CSV tables for paper tables
4. Reference JSON metrics in Results section

Generated: $(date)
EOF

echo "✓ Summary report generated: results/pipeline_summary.md"

echo ""
echo "======================================="
echo "Full pipeline completed successfully!"
echo "Check results/ directory for all generated files."
echo "Figures copied to paper/figures/ for LaTeX compilation."
echo "======================================="
