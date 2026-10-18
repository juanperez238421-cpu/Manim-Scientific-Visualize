# Arranca la API solo en loopback (sin puertos entrantes en el router).
$Root = Split-Path $PSScriptRoot -Parent; Set-Location $Root
$py = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path ".env")) { Write-Host "Falta .env (copia .env.example)." -ForegroundColor Red; exit 1 }
$h = (Select-String -Path .env -Pattern '^API_HOST=(.*)$').Matches.Groups[1].Value; if (-not $h) { $h = "127.0.0.1" }
$p = (Select-String -Path .env -Pattern '^API_PORT=(.*)$').Matches.Groups[1].Value; if (-not $p) { $p = "8000" }
& $py -m uvicorn api.app.main:app --host $h --port $p
