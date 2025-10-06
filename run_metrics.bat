@echo off
REM Windows batch script equivalent to Makefile
REM Run all metrics experiments for Triality-HDC

echo Running Triality v2.0 Metrics Pipeline...
echo ========================================

echo.
echo [1/3] Running phi vs rational bicoherence metrics...
python -m experiments.phi_vs_rational_metrics
if %errorlevel% neq 0 (
    echo ERROR: phi_vs_rational_metrics failed
    exit /b 1
)

echo.
echo [2/3] Running Koopman gap metrics...
python -m experiments.koopman_gap_metrics
if %errorlevel% neq 0 (
    echo ERROR: koopman_gap_metrics failed
    exit /b 1
)

echo.
echo [3/3] Running latency fit metrics...
python -m experiments.latency_fit_metrics
if %errorlevel% neq 0 (
    echo ERROR: latency_fit_metrics failed
    exit /b 1
)

echo.
echo ========================================
echo All metrics experiments completed successfully!
echo Check results/ directory for generated JSON files and figures.
echo ========================================
