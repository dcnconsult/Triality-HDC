#!/bin/bash
# Linux/Unix shell script equivalent to Makefile metrics
# Run all metrics experiments for Triality-HDC

echo "Running Triality v2.0 Metrics Pipeline..."
echo "========================================"

# Ensure results directory exists
mkdir -p results

echo ""
echo "[1/3] Running phi vs rational bicoherence metrics..."
python -m experiments.phi_vs_rational_metrics
if [ $? -ne 0 ]; then
    echo "ERROR: phi_vs_rational_metrics failed"
    exit 1
fi
echo "✓ phi_vs_rational_metrics completed"

echo ""
echo "[2/3] Running Koopman gap metrics..."
python -m experiments.koopman_gap_metrics
if [ $? -ne 0 ]; then
    echo "ERROR: koopman_gap_metrics failed"
    exit 1
fi
echo "✓ koopman_gap_metrics completed"

echo ""
echo "[3/3] Running latency fit metrics..."
python -m experiments.latency_fit_metrics
if [ $? -ne 0 ]; then
    echo "ERROR: latency_fit_metrics failed"
    exit 1
fi
echo "✓ latency_fit_metrics completed"

echo ""
echo "========================================"
echo "All metrics experiments completed successfully!"
echo "Check results/ directory for generated JSON files and figures."
echo "========================================"
