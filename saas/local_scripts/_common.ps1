# Funciones compartidas por los scripts de AniMotionPDF (se importan con:  . "$PSScriptRoot\_common.ps1")
$ErrorActionPreference = "Continue"   # los comandos nativos que escriben en stderr no deben abortar el script; se comprueba $LASTEXITCODE
$script:Root = Split-Path $PSScriptRoot -Parent
Set-Location $script:Root
$script:Py = Join-Path $script:Root ".venv\Scripts\python.exe"

function Have($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }

# Lee KEY=VALUE de un archivo .env (sin imprimir valores). Devuelve un hashtable.
function Read-DotEnv([string]$Path) {
  $h = @{}
  if (-not (Test-Path $Path)) { return $h }
  foreach ($line in Get-Content -LiteralPath $Path -Encoding UTF8) {
    if ($line -match '^\s*#' -or $line -notmatch '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=(.*)$') { continue }
    $v = $Matches[2].Trim()
    if ($v.Length -ge 2 -and (($v.StartsWith('"') -and $v.EndsWith('"')) -or ($v.StartsWith("'") -and $v.EndsWith("'")))) { $v = $v.Substring(1, $v.Length - 2) }
    $h[$Matches[1]] = $v
  }
  return $h
}

# Carga las variables del .env en el entorno del proceso actual (los hijos las heredan).
function Import-DotEnv([string]$Path) {
  $h = Read-DotEnv $Path
  foreach ($k in $h.Keys) { Set-Item -Path "Env:$k" -Value $h[$k] }
  return $h
}

# Agrega KEY=VALUE al .env SOLO si la clave no existe (nunca sobrescribe ni imprime valores).
function Add-EnvIfMissing([string]$Path, [string]$Key, [string]$Value) {
  $cur = Read-DotEnv $Path
  if ($cur.ContainsKey($Key) -and $cur[$Key] -ne "") { return $false }
  if ($cur.ContainsKey($Key)) {
    $txt = (Get-Content -LiteralPath $Path -Raw -Encoding UTF8) -replace "(?m)^\s*$([regex]::Escape($Key))\s*=.*$", "$Key=$Value"
    [System.IO.File]::WriteAllText($Path, $txt, (New-Object System.Text.UTF8Encoding($false)))
  } else {
    [System.IO.File]::AppendAllText($Path, "`n$Key=$Value`n", (New-Object System.Text.UTF8Encoding($false)))
  }
  return $true
}

function New-Secret([int]$Bytes = 32) {
  $b = New-Object byte[] $Bytes
  [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b)
  return ([Convert]::ToBase64String($b) -replace '[^A-Za-z0-9]', '').Substring(0, [Math]::Min($Bytes, 40))
}

function Find-PgBin {
  $c = Get-Command pg_ctl -ErrorAction SilentlyContinue
  if ($c) { return Split-Path $c.Source -Parent }
  foreach ($base in @("C:\Program Files\PostgreSQL", "C:\Program Files (x86)\PostgreSQL")) {
    if (Test-Path $base) {
      $d = Get-ChildItem $base -Directory | Sort-Object { [int]($_.Name -replace '\D', '') } -Descending | Select-Object -First 1
      if ($d -and (Test-Path (Join-Path $d.FullName "bin\pg_ctl.exe"))) { return (Join-Path $d.FullName "bin") }
    }
  }
  return $null
}

function Test-Port([int]$Port) {
  try { $c = New-Object System.Net.Sockets.TcpClient; $c.Connect("127.0.0.1", $Port); $c.Close(); return $true } catch { return $false }
}

function Wait-Http([string]$Url, [int]$Seconds = 60) {
  $end = (Get-Date).AddSeconds($Seconds)
  while ((Get-Date) -lt $end) {
    try { $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3; if ($r.StatusCode -lt 500) { return $true } } catch { }
    Start-Sleep -Milliseconds 700
  }
  return $false
}
