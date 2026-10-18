# Prueba minima de Claude API desde Windows nativo, a traves del AIBudgetGuard (una sola llamada, maximo 0,25 USD).
# Uso:  .\scripts\smoke_claude.ps1 -DryRun    (sin llamar a la API)   |   .\scripts\smoke_claude.ps1
param([switch]$DryRun)
$Root = Split-Path $PSScriptRoot -Parent; Set-Location $Root
$py = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) { Write-Host "Falta .venv: ejecuta primero scripts\setup.ps1" -ForegroundColor Red; exit 1 }
if ($DryRun) { & $py scripts\smoke_claude_call.py --dry-run } else { & $py scripts\smoke_claude_call.py }
