<#
  AniMotionPDF - preparacion local (sin administrador, sin instalar nada global).
  Hace: venv en .\.venv, dependencias pip, clona el motor pdf2video en .\engine (sparse, solo pdf2video/),
        crea .env desde .env.example SI NO EXISTE (sin clave). Las herramientas del sistema faltantes solo se REPORTAN.
  Uso:  powershell -NoProfile -File .\scripts\setup.ps1
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root
function Have($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }

$missing = @()
if (-not (Have python)) { $missing += "winget install Python.Python.3.12" }
if (-not (Have git))    { $missing += "winget install Git.Git" }
if (-not (Have ffmpeg)) { $missing += "winget install Gyan.FFmpeg" }
if (-not (Have latex))  { $missing += "winget install MiKTeX.MiKTeX   (amsmath, amssymb, mathpazo, dvisvgm)" }
if ($missing.Count) { Write-Host "Faltan herramientas (instalalas tu y vuelve a ejecutar):" -ForegroundColor Yellow; $missing | % { "  $_" }; exit 10 }

if (-not (Test-Path ".venv")) { python -m venv .venv }
$py = Join-Path $Root ".venv\Scripts\python.exe"
& $py -m pip install --upgrade pip | Out-Null
& $py -m pip install -r requirements.txt

if (-not (Test-Path "engine\pdf2video")) {
  git clone --depth 1 --filter=blob:none --sparse https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize.git engine\_clone
  git -C engine\_clone sparse-checkout set pdf2video
  Move-Item engine\_clone\pdf2video engine\pdf2video
  git -C engine\_clone rev-parse HEAD | Set-Content engine\ENGINE_COMMIT.txt
  Remove-Item engine\_clone -Recurse -Force
}
# ManimCE 0.22 necesita Pillow < 13 (Image.fromarray(mode=...)); pdfplumber exige >= 12.2
& $py -m pip install -r engine\pdf2video\requirements.txt "pillow>=12.2,<13"
& $py -m pip check
& $py scripts\apply_engine_patches.py          # E/S UTF-8 explicita en el motor (idempotente)

if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env"; Write-Host "Creado .env: abrelo y pon tu ANTHROPIC_API_KEY y ANIMOTION_MODEL." -ForegroundColor Cyan }
Write-Host "Listo. Siguiente: .\scripts\test.ps1  y luego  .\scripts\run_api.ps1"
