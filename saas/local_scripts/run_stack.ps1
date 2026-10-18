<#
  AniMotionPDF - arranca el SaaS LOCAL completo: PostgreSQL + API SaaS (8000) + worker + frontend Next.js (3000).
  Solo escucha en 127.0.0.1 (sin puertos entrantes en el router). Logs en .\storage\logs.
  -NoFrontend   no arranca Next.js          -Provider replay|anthropic   fuerza el proveedor del worker
  Uso:  powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_stack.ps1
#>
param([switch]$NoFrontend, [string]$Provider = "")
. "$PSScriptRoot\_common.ps1"
$cfg = Import-DotEnv (Join-Path $Root ".env")
if ($Provider) { $env:ANIMOTION_PROVIDER = $Provider }
foreach ($k in "DATABASE_URL", "WORKER_TOKEN", "STORAGE_SIGNING_SECRET", "LOCAL_STORAGE_DIR") {
  if (-not $cfg[$k]) { Write-Host "Falta $k en .env: ejecuta .\scripts\setup_saas.ps1" -ForegroundColor Red; exit 1 }
}
if (-not $cfg["CLERK_JWKS_URL"]) { Write-Host "AVISO: Clerk no está configurado; el login del frontend no funcionará (usa scripts\e2e_backend.ps1 para probar el backend)." -ForegroundColor Yellow }
$logs = Join-Path $Root "storage\logs"; New-Item -ItemType Directory -Force -Path $logs | Out-Null

if (-not (Test-Port 54329)) {
  $pgbin = Find-PgBin
  if (-not $pgbin) { Write-Host "PostgreSQL no encontrado: ejecuta setup_saas.ps1" -ForegroundColor Red; exit 1 }
  & (Join-Path $pgbin "pg_ctl.exe") -D (Join-Path $Root "storage\pgdata") -o "-p 54329 -c listen_addresses=127.0.0.1" -l (Join-Path $logs "postgres.log") -w start | Out-Null
  if (-not (Test-Port 54329)) { Write-Host "PostgreSQL no arrancó" -ForegroundColor Red; exit 1 }
}
if (Test-Port 8000) { Write-Host "El puerto 8000 ya está en uso: ¿stack ya iniciado? (.\scripts\stop_stack.ps1)" -ForegroundColor Yellow; exit 1 }

$pids = @{}
$api = Start-Process -FilePath $Py -ArgumentList "-m", "uvicorn", "app.main:create_app", "--factory", "--host", "127.0.0.1", "--port", "8000" `
  -WorkingDirectory (Join-Path $Root "saas\apps\api") -RedirectStandardOutput (Join-Path $logs "api.out.log") -RedirectStandardError (Join-Path $logs "api.err.log") -WindowStyle Hidden -PassThru
$pids["api"] = $api.Id
if (-not (Wait-Http "http://127.0.0.1:8000/healthz" 60)) { Write-Host "La API no respondió; revisa storage\logs\api.err.log" -ForegroundColor Red; exit 1 }

$env:PYTHONPATH = "$Root\packages\scianim_adapter;$Root\worker"
$wk = Start-Process -FilePath $Py -ArgumentList "-m", "animotion_worker", "run" -WorkingDirectory $Root `
  -RedirectStandardOutput (Join-Path $logs "worker.out.log") -RedirectStandardError (Join-Path $logs "worker.err.log") -WindowStyle Hidden -PassThru
$pids["worker"] = $wk.Id

if (-not $NoFrontend) {
  $fe = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "npm run dev" -WorkingDirectory (Join-Path $Root "frontend") `
    -RedirectStandardOutput (Join-Path $logs "frontend.out.log") -RedirectStandardError (Join-Path $logs "frontend.err.log") -WindowStyle Hidden -PassThru
  $pids["frontend"] = $fe.Id
}
$pids | ConvertTo-Json | Set-Content (Join-Path $Root "storage\pids.json")
Start-Sleep -Seconds 3
Write-Host "API      http://127.0.0.1:8000/healthz"
Write-Host "Worker   proveedor=$($env:ANIMOTION_PROVIDER)  (storage\logs\worker.out.log)"
if (-not $NoFrontend) { Write-Host "Frontend http://localhost:3000   (la primera compilación tarda ~30-60 s)" }
Write-Host "Detener: .\scripts\stop_stack.ps1"
