# PowerShell script equivalent to Makefile
# Run all metrics experiments for Triality-HDC

Write-Host "Running Triality v2.0 Metrics Pipeline..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host ""
Write-Host "[1/3] Running phi vs rational bicoherence metrics..." -ForegroundColor Yellow
python -m experiments.phi_vs_rational_metrics
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: phi_vs_rational_metrics failed" -ForegroundColor Red
    exit 1
}
Write-Host "phi_vs_rational_metrics completed" -ForegroundColor Green

Write-Host ""
Write-Host "[2/3] Running Koopman gap metrics..." -ForegroundColor Yellow
python -m experiments.koopman_gap_metrics
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: koopman_gap_metrics failed" -ForegroundColor Red
    exit 1
}
Write-Host "koopman_gap_metrics completed" -ForegroundColor Green

Write-Host ""
Write-Host "[3/3] Running latency fit metrics..." -ForegroundColor Yellow
python -m experiments.latency_fit_metrics
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: latency_fit_metrics failed" -ForegroundColor Red
    exit 1
}
Write-Host "latency_fit_metrics completed" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "All metrics experiments completed successfully!" -ForegroundColor Green
Write-Host "Check results/ directory for generated JSON files and figures." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green