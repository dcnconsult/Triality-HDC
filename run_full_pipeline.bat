@echo off
REM Complete Triality pipeline - equivalent to make full

echo Triality v2.0 - Full Pipeline Execution
echo =======================================

echo.
echo [1/5] Running core metrics...
python -m experiments.phi_vs_rational_metrics
if %errorlevel% neq 0 (
    echo ERROR: phi_vs_rational_metrics failed
    exit /b 1
)
echo ✓ phi_vs_rational_metrics completed

python -m experiments.koopman_gap_metrics
if %errorlevel% neq 0 (
    echo ERROR: koopman_gap_metrics failed
    exit /b 1
)
echo ✓ koopman_gap_metrics completed

python -m experiments.latency_fit_metrics
if %errorlevel% neq 0 (
    echo ERROR: latency_fit_metrics failed
    exit /b 1
)
echo ✓ latency_fit_metrics completed

echo.
echo [2/5] Running ablations...
python -m experiments.ablations
if %errorlevel% neq 0 (
    echo ERROR: ablations failed
    exit /b 1
)
echo ✓ ablations completed

echo.
echo [3/5] Running aggregation...
python -m scripts.aggregate
if %errorlevel% neq 0 (
    echo ERROR: aggregation failed
    exit /b 1
)
echo ✓ aggregation completed

echo.
echo [4/5] Copying figures to paper/figures/...
if exist "results\bico_phi.png" (
    copy "results\bico_phi.png" "paper\figures\bico_phi_placeholder.png" >nul
    echo ✓ Copied bico_phi.png
) else (
    echo ⚠ Warning: bico_phi.png not found
)

if exist "results\bico_rational.png" (
    copy "results\bico_rational.png" "paper\figures\bico_rational_placeholder.png" >nul
    echo ✓ Copied bico_rational.png
) else (
    echo ⚠ Warning: bico_rational.png not found
)

if exist "results\koopman_hist.png" (
    copy "results\koopman_hist.png" "paper\figures\koop_hist_placeholder.png" >nul
    echo ✓ Copied koopman_hist.png
) else (
    echo ⚠ Warning: koopman_hist.png not found
)

if exist "results\latency_fit.png" (
    copy "results\latency_fit.png" "paper\figures\latency_placeholder.png" >nul
    echo ✓ Copied latency_fit.png
) else (
    echo ⚠ Warning: latency_fit.png not found
)

echo.
echo [5/5] Pipeline completed successfully!
echo.
echo Generated files:
echo - JSON metrics in results/
echo - CSV tables in results/
echo - Figures copied to paper/figures/
echo.
echo Next steps:
echo 1. Review figures in paper/figures/
echo 2. Compile preprint.tex
echo 3. Use CSV tables for paper tables
echo.
pause
