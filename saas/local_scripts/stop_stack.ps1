# Detiene API, worker y frontend iniciados por run_stack.ps1 (árbol de procesos completo). -Postgres también detiene PostgreSQL.
param([switch]$Postgres)
. "$PSScriptRoot\_common.ps1"
$f = Join-Path $Root "storage\pids.json"
if (Test-Path $f) {
  $p = Get-Content $f -Raw | ConvertFrom-Json
  foreach ($n in $p.PSObject.Properties.Name) { & taskkill /F /T /PID $p.$n 2>$null | Out-Null; Write-Host "detenido $n" }
  Remove-Item $f -Force
}
if ($Postgres) {
  $pgbin = Find-PgBin
  if ($pgbin) { & (Join-Path $pgbin "pg_ctl.exe") -D (Join-Path $Root "storage\pgdata") -m fast stop | Out-Null; Write-Host "PostgreSQL detenido" }
}
