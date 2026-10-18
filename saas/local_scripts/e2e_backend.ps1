<#
  AniMotionPDF - recorrido E2E del BACKEND sin Clerk: PDF -> subida firmada -> estimación -> reserva -> worker -> motor -> MP4
  -> descarga/Range -> ffprobe + decodificación completa. Usa un IdP de DESARROLLO (no es Clerk) y una BD aparte (animotion_e2e).
  Por defecto el proveedor de IA es SIMULADO (replay): NO gasta Anthropic. Para gastar de verdad hay que pasar -AllowRealClaude.
  Ejemplos:
    .\scripts\e2e_backend.ps1 -Pdf <ruta.pdf> -ReplaySpec <spec.json> -Resolution 720p
    .\scripts\e2e_backend.ps1 -Pdf <ruta.pdf> -Resolution 1080p -AllowRealClaude        (UNA llamada real, sujeta a AIBudgetGuard)
#>
param(
  [Parameter(Mandatory = $true)][string]$Pdf,
  [string]$ReplaySpec = "",
  [ValidateSet("480p", "720p", "1080p")][string]$Resolution = "480p",
  [string]$Plan = "starter",
  [int]$Seconds = 60,
  [switch]$AllowRealClaude,
  [double]$CancelAfter = -1,
  [string]$Expect = "succeeded",
  [string]$Tag = ""
)
. "$PSScriptRoot\_common.ps1"
$null = Import-DotEnv (Join-Path $Root ".env")
if (-not (Test-Path $Pdf)) { Write-Host "No existe el PDF: $Pdf" -ForegroundColor Red; exit 1 }
$Pdf = (Resolve-Path $Pdf).Path
if ($AllowRealClaude) { $env:ANIMOTION_PROVIDER = "anthropic" }
else {
  if (-not $ReplaySpec) { Write-Host "Sin -AllowRealClaude se necesita -ReplaySpec <spec.json> (proveedor simulado)." -ForegroundColor Red; exit 1 }
  $env:ANIMOTION_PROVIDER = "replay"; $env:ANIMOTION_REPLAY_SPEC = (Resolve-Path $ReplaySpec).Path
}
if (-not $env:E2E_DATABASE_URL) { Write-Host "Falta E2E_DATABASE_URL: ejecuta setup_saas.ps1" -ForegroundColor Red; exit 1 }
$env:DATABASE_URL = $env:E2E_DATABASE_URL
$ev = Join-Path $Root ("storage\evidence\e2e_" + (Get-Date -Format "yyyyMMdd_HHmmss") + "_" + $Resolution + $Tag); New-Item -ItemType Directory -Force -Path $ev | Out-Null
$e2eBlobs = ((Join-Path $Root "storage\e2e_blobs") -replace '\\', '/')
$IdpPort = 9100; $ApiPort = 8100
$env:CLERK_JWKS_URL = "http://127.0.0.1:$IdpPort/jwks.json"; $env:CLERK_ISSUER = "http://127.0.0.1:$IdpPort"; $env:CLERK_AUTHORIZED_PARTIES = ""
$env:PUBLIC_BASE_URL = "http://127.0.0.1:$ApiPort"; $env:SAAS_API_URL = $env:PUBLIC_BASE_URL; $env:LOCAL_STORAGE_DIR = $e2eBlobs
$env:WORKER_WORK_DIR = (Join-Path $Root "storage\worker_e2e"); $env:WORKER_ID = "e2e-worker-1"; $env:WORKER_POLL_SECONDS = "1"
$env:PYTHONPATH = "$Root\packages\scianim_adapter;$Root\worker"
$procs = @()
try {
  & $Py saas\apps\api\scripts\migrate.py --seed-dev-plans
  $procs += Start-Process -FilePath $Py -ArgumentList "saas\apps\api\scripts\dev_jwks.py", "$IdpPort" -WorkingDirectory $Root -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $ev "idp.out.log") -RedirectStandardError (Join-Path $ev "idp.err.log")
  $procs += Start-Process -FilePath $Py -ArgumentList "-m", "uvicorn", "app.main:create_app", "--factory", "--host", "127.0.0.1", "--port", "$ApiPort" `
    -WorkingDirectory (Join-Path $Root "saas\apps\api") -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $ev "api.out.log") -RedirectStandardError (Join-Path $ev "api.err.log")
  if (-not (Wait-Http "http://127.0.0.1:$ApiPort/healthz" 60)) { throw "la API de pruebas no arrancó (ver $ev\api.err.log)" }
  $tok = (Invoke-WebRequest -Uri "http://127.0.0.1:$IdpPort/token?sub=user_e2e" -UseBasicParsing).Content
  Invoke-WebRequest -Uri "http://127.0.0.1:$ApiPort/v1/me" -Headers @{ Authorization = "Bearer $tok" } -UseBasicParsing | Out-Null
  & $Py saas\apps\api\scripts\migrate.py --grant-credits user_e2e@dev.test 5000
  & $Py saas\apps\api\scripts\migrate.py --set-plan user_e2e@dev.test $Plan
  $procs += Start-Process -FilePath $Py -ArgumentList "-m", "animotion_worker", "run" -WorkingDirectory $Root -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $ev "worker.out.log") -RedirectStandardError (Join-Path $ev "worker.err.log")
  $args2 = @("scripts\e2e_local.py", "--api", "http://127.0.0.1:$ApiPort", "--idp", "http://127.0.0.1:$IdpPort", "--sub", "user_e2e", "--pdf", $Pdf,
             "--resolution", $Resolution, "--seconds", "$Seconds", "--timeout", "7200", "--expect", $Expect,
             "--out", (Join-Path $ev "report.json"), "--download", (Join-Path $ev "video.mp4"))
  if ($CancelAfter -ge 0) { $args2 += @("--cancel-after", "$CancelAfter") }
  $sw = [Diagnostics.Stopwatch]::StartNew()
  & $Py @args2 2>&1 | Tee-Object -FilePath (Join-Path $ev "e2e.log")
  $code = $LASTEXITCODE; $sw.Stop()
  "wall_seconds=$([math]::Round($sw.Elapsed.TotalSeconds,1))" | Add-Content (Join-Path $ev "e2e.log")
  Write-Host "`nEvidencia en: $ev   (exit=$code)" -ForegroundColor Cyan
  exit $code
}
finally {
  foreach ($p in $procs) { if ($p -and -not $p.HasExited) { & taskkill /F /T /PID $p.Id 2>$null | Out-Null } }
}
