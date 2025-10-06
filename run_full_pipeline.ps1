# PowerShell script for complete Triality pipeline
# Equivalent to: make full

Write-Host "Triality v2.0 - Full Pipeline Execution" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

# Ensure results directory exists
New-Item -ItemType Directory -Force -Path "results" | Out-Null

Write-Host ""
Write-Host "[1/5] Running core metrics..." -ForegroundColor Yellow

# Phi metrics
Write-Host "  Running phi_vs_rational_metrics..." -ForegroundColor Cyan
python -m experiments.phi_vs_rational_metrics
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: phi_vs_rational_metrics failed" -ForegroundColor Red
    exit 1
}
Write-Host "  phi_vs_rational_metrics completed" -ForegroundColor Green

# Koopman metrics
Write-Host "  Running koopman_gap_metrics..." -ForegroundColor Cyan
python -m experiments.koopman_gap_metrics
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: koopman_gap_metrics failed" -ForegroundColor Red
    exit 1
}
Write-Host "  koopman_gap_metrics completed" -ForegroundColor Green

# Latency metrics
Write-Host "  Running latency_fit_metrics..." -ForegroundColor Cyan
python -m experiments.latency_fit_metrics
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: latency_fit_metrics failed" -ForegroundColor Red
    exit 1
}
Write-Host "  latency_fit_metrics completed" -ForegroundColor Green

Write-Host ""
Write-Host "[2/5] Running ablations..." -ForegroundColor Yellow
python -m experiments.ablations
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: ablations failed" -ForegroundColor Red
    exit 1
}
Write-Host "ablations completed" -ForegroundColor Green

Write-Host ""
Write-Host "[3/5] Running aggregation..." -ForegroundColor Yellow
python -m scripts.aggregate
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: aggregation failed" -ForegroundColor Red
    exit 1
}
Write-Host "aggregation completed" -ForegroundColor Green

Write-Host ""
Write-Host "[4/5] Copying figures to paper/figures/..." -ForegroundColor Yellow

# Copy figures to paper directory
$figures = @{
    "results/bico_phi.png" = "paper/figures/bico_phi_placeholder.png"
    "results/bico_rational.png" = "paper/figures/bico_rational_placeholder.png"
    "results/koopman_hist.png" = "paper/figures/koop_hist_placeholder.png"
    "results/latency_fit.png" = "paper/figures/latency_placeholder.png"
}

foreach ($source in $figures.Keys) {
    $dest = $figures[$source]
    if (Test-Path $source) {
        Copy-Item $source $dest -Force
        Write-Host "  Copied $source -> $dest" -ForegroundColor Green
    } else {
        Write-Host "  Warning: $source not found" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "[5/5] Pipeline completed successfully!" -ForegroundColor Green
Write-Host "Check results/ directory for all generated files." -ForegroundColor Cyan
Write-Host "Figures copied to paper/figures/ for LaTeX compilation." -ForegroundColor Cyan
