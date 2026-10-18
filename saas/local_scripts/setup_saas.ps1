<#
  AniMotionPDF - M2: prepara el SaaS LOCAL (sin administrador, sin pagos, sin servicios externos de pago).
  Hace (idempotente, nunca sobrescribe valores existentes del .env, nunca imprime secretos):
    1) pip install -r requirements.txt  y parches del motor (UTF-8 + español/coma decimal/perfiles).
    2) PostgreSQL LOCAL portable en .\storage\pgdata (puerto 54329, solo 127.0.0.1) usando los binarios de PostgreSQL ya instalados.
    3) Completa .env con las variables del SaaS (URL de BD, secretos aleatorios, almacenamiento local, CORS).
    4) Deriva CLERK_ISSUER / CLERK_JWKS_URL desde la clave PUBLICA de Clerk Development (frontend\.env.local).
    5) Aplica migraciones y planes BORRADOR de desarrollo.
    6) npm install del frontend.
  Uso:  powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup_saas.ps1
#>
. "$PSScriptRoot\_common.ps1"
$EnvFile = Join-Path $Root ".env"
$Fe = Join-Path $Root "frontend"
if (-not (Test-Path $Py)) { Write-Host "Falta .venv: ejecuta primero .\scripts\setup.ps1" -ForegroundColor Red; exit 10 }
if (-not (Test-Path $EnvFile)) { Copy-Item (Join-Path $Root ".env.example") $EnvFile }

Write-Host "1/6 Dependencias Python y parches del motor..." -ForegroundColor Cyan
& $Py -m pip install -r requirements.txt | Out-Null
& $Py scripts\apply_engine_patches.py
& $Py scripts\apply_engine_patches_m2.py
New-Item -ItemType Directory -Force -Path storage\logs, storage\blobs, storage\worker | Out-Null

Write-Host "2/6 PostgreSQL local..." -ForegroundColor Cyan
$PgPort = 54329
$pgbin = Find-PgBin
if (-not $pgbin) {
  Write-Host "No se encontró PostgreSQL. Instálalo (gratuito) y vuelve a ejecutar:" -ForegroundColor Yellow
  Write-Host "  winget install PostgreSQL.PostgreSQL.16      (el servicio de Windows que crea NO se usa; solo se usan sus binarios)"
  exit 10
}
$data = Join-Path $Root "storage\pgdata"
Add-EnvIfMissing $EnvFile "PG_LOCAL_PASSWORD" (New-Secret 24) | Out-Null
$pgpw = (Read-DotEnv $EnvFile)["PG_LOCAL_PASSWORD"]
if (-not (Test-Path (Join-Path $data "PG_VERSION"))) {
  $pwf = Join-Path $env:TEMP ("pgpw_" + [guid]::NewGuid().ToString("N"))
  [System.IO.File]::WriteAllText($pwf, $pgpw)
  try { & (Join-Path $pgbin "initdb.exe") -D $data -U postgres -A scram-sha-256 --pwfile=$pwf -E UTF8 --locale=C | Out-Null }
  finally { Remove-Item $pwf -Force -ErrorAction SilentlyContinue }
  if ($LASTEXITCODE -ne 0) { Write-Host "initdb falló" -ForegroundColor Red; exit 1 }
}
if (-not (Test-Port $PgPort)) {
  & (Join-Path $pgbin "pg_ctl.exe") -D $data -o "-p $PgPort -c listen_addresses=127.0.0.1" -l (Join-Path $Root "storage\logs\postgres.log") -w start | Out-Null
  if (-not (Test-Port $PgPort)) { Write-Host "PostgreSQL no arrancó: revisa storage\logs\postgres.log" -ForegroundColor Red; exit 1 }
}
$env:PGPASSWORD = $pgpw
foreach ($db in @("animotion", "animotion_e2e")) {
  $exists = & (Join-Path $pgbin "psql.exe") -h 127.0.0.1 -p $PgPort -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$db'"
  if (-not $exists) { & (Join-Path $pgbin "createdb.exe") -h 127.0.0.1 -p $PgPort -U postgres $db }
}
Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue

Write-Host "3/6 Variables del SaaS en .env (solo las que faltan)..." -ForegroundColor Cyan
$blobs = (Join-Path $Root "storage\blobs") -replace '\\', '/'
$pairs = [ordered]@{
  "DATABASE_URL"            = "postgresql://postgres:$pgpw@127.0.0.1:$PgPort/animotion"
  "E2E_DATABASE_URL"        = "postgresql://postgres:$pgpw@127.0.0.1:$PgPort/animotion_e2e"
  "LOCAL_STORAGE_DIR"       = $blobs
  "STORAGE_SIGNING_SECRET"  = (New-Secret 32)
  "PUBLIC_BASE_URL"         = "http://127.0.0.1:8000"
  "WORKER_TOKEN"            = (New-Secret 40)
  "SAAS_API_URL"            = "http://127.0.0.1:8000"
  "CORS_ORIGINS"            = "http://localhost:3000,http://127.0.0.1:3000"
  "CLERK_AUTHORIZED_PARTIES"= "http://localhost:3000"
  "ANIMOTION_PROVIDER"      = "anthropic"
  "WORKER_WORK_DIR"         = "./storage/worker"
}
foreach ($k in $pairs.Keys) { if (Add-EnvIfMissing $EnvFile $k $pairs[$k]) { Write-Host "  + $k" } }

Write-Host "4/6 Clerk Development..." -ForegroundColor Cyan
$feEnv = Join-Path $Fe ".env.local"
if (-not (Test-Path $feEnv)) {
  Copy-Item (Join-Path $Fe ".env.example") $feEnv
  Write-Host "  Se creó frontend\.env.local. Créa una aplicación en https://dashboard.clerk.com (instancia DEVELOPMENT, gratis) y pega" -ForegroundColor Yellow
  Write-Host "  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY (pk_test_...) y CLERK_SECRET_KEY (sk_test_...) en ese archivo. NO las pegues en el chat."
}
$fe = Read-DotEnv $feEnv
$pk = $fe["NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY"]
$clerkReady = $false
if ($pk -and $pk.StartsWith("pk_test_") -and $fe["CLERK_SECRET_KEY"] -and $fe["CLERK_SECRET_KEY"].StartsWith("sk_test_")) {
  $b64 = $pk.Substring(8); while ($b64.Length % 4) { $b64 += "=" }
  $domain = ([System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b64))).TrimEnd('$')
  if ($domain -match '^[a-z0-9.-]+\.[a-z]{2,}$') {
    Add-EnvIfMissing $EnvFile "CLERK_ISSUER" "https://$domain" | Out-Null
    Add-EnvIfMissing $EnvFile "CLERK_JWKS_URL" "https://$domain/.well-known/jwks.json" | Out-Null
    $clerkReady = $true
    Write-Host "  Clerk Development detectado (dominio $domain)."
  }
} elseif ($pk -and $pk.StartsWith("pk_live_")) {
  Write-Host "  ERROR: pk_live_ detectada. Esta fase usa SOLO Clerk Development (pk_test_/sk_test_)." -ForegroundColor Red; exit 1
}
if (-not $clerkReady) { Write-Host "  Clerk NO configurado todavía (el backend y el E2E sin Clerk funcionan igual: scripts\e2e_backend.ps1)." -ForegroundColor Yellow }
Add-EnvIfMissing $feEnv "FASTAPI_URL" "http://127.0.0.1:8000" | Out-Null

Write-Host "5/6 Migraciones..." -ForegroundColor Cyan
$null = Import-DotEnv $EnvFile
& $Py saas\apps\api\scripts\migrate.py --seed-dev-plans
if ($LASTEXITCODE -ne 0) { Write-Host "Migración falló" -ForegroundColor Red; exit 1 }

Write-Host "6/6 Frontend (npm install)..." -ForegroundColor Cyan
if (-not (Have node)) { Write-Host "  Falta Node.js >= 20.9:  winget install OpenJS.NodeJS.LTS" -ForegroundColor Yellow }
elseif (-not (Test-Path (Join-Path $Fe "node_modules"))) { Push-Location $Fe; npm install --no-audit --no-fund; Pop-Location }
Write-Host "`nListo. Siguiente:  .\scripts\test.ps1   y luego   .\scripts\run_stack.ps1" -ForegroundColor Green
