<#
  AniMotionPDF - M1 on Windows: environment preflight + pdf2video engine tests + measured preview/final render.

  STATUS: NOT RUN (written on Linux; no Windows shell was available). Read it before running.
  It installs nothing system-wide by itself: missing tools are only REPORTED (with the winget command to
  run yourself). It creates ONE new folder, never touches OpenClaw, Supabase or global settings.

  Usage (PowerShell, no admin needed):
      powershell -ExecutionPolicy Bypass -File .\m1_setup_and_run.ps1 [-Work "$env:USERPROFILE\animotion-m1"] [-Pdf C:\path\worksheet.pdf -Spec C:\path\spec.json] [-SkipFinal] [-Shutdown]

  -Pdf/-Spec  use your own MRU worksheet + its spec (default: the engine's physics example).
  -SkipFinal  stop after tests + 480p preview (about 1-2 min) and skip the 1080p30 final render.
  -Shutdown   at the very end, wait 60 s and shut Windows down (cancel with:  shutdown /a ).
#>
param(
  [string]$Work = "$env:USERPROFILE\animotion-m1",
  [string]$Pdf = "",
  [string]$Spec = "",
  [switch]$SkipFinal,
  [switch]$Shutdown
)
$ErrorActionPreference = "Stop"
$log = Join-Path $Work "m1.log"
New-Item -ItemType Directory -Force -Path $Work | Out-Null
Start-Transcript -Path $log -Append | Out-Null

function Have($c) { return [bool](Get-Command $c -ErrorAction SilentlyContinue) }
function Ver($c, $a) { try { (& $c $a 2>&1 | Select-Object -First 1) -join "" } catch { "ERROR" } }

# ---------------------------------------------------------------- 1. preflight (read-only)
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$gpu = Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion
$os  = Get-CimInstance Win32_OperatingSystem
$env_report = [ordered]@{
  collected_utc = (Get-Date).ToUniversalTime().ToString("o")
  os            = "$($os.Caption) $($os.Version) build $($os.BuildNumber)"
  cpu           = $cpu.Name
  cores         = $cpu.NumberOfCores
  threads       = $cpu.NumberOfLogicalProcessors
  ram_gb        = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
  gpus          = @($gpu)
  nvidia_smi    = $(if (Have nvidia-smi) { (& nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader) } else { $null })
  python        = $(if (Have python) { Ver python "--version" } else { $null })
  git           = $(if (Have git) { Ver git "--version" } else { $null })
  ffmpeg        = $(if (Have ffmpeg) { Ver ffmpeg "-version" } else { $null })
  latex         = $(if (Have latex) { Ver latex "--version" } else { $null })
  dvisvgm       = $(if (Have dvisvgm) { Ver dvisvgm "--version" } else { $null })
  tesseract     = $(if (Have tesseract) { Ver tesseract "--version" } else { $null })
}
$env_report | ConvertTo-Json -Depth 4 | Set-Content -Encoding utf8 (Join-Path $Work "benchmark_environment.json")
$env_report | ConvertTo-Json -Depth 4

$missing = @()
if (-not (Have python))   { $missing += "winget install Python.Python.3.12" }
if (-not (Have git))      { $missing += "winget install Git.Git" }
if (-not (Have ffmpeg))   { $missing += "winget install Gyan.FFmpeg" }
if (-not (Have latex) -or -not (Have dvisvgm)) { $missing += "winget install MiKTeX.MiKTeX   (needs amsmath, amssymb, mathpazo, dvisvgm)" }
if (-not (Have tesseract)){ $missing += "winget install UB-Mannheim.TesseractOCR   (only needed for scanned PDFs)" }
if ($missing.Count) {
  Write-Host "`nMISSING TOOLS (install them yourself, then re-run; verify ids with 'winget search'):" -ForegroundColor Yellow
  $missing | ForEach-Object { Write-Host "  $_" }
  Stop-Transcript | Out-Null
  exit 10
}
if (-not (Get-ChildItem "C:\Windows\Fonts","$env:LOCALAPPDATA\Microsoft\Windows\Fonts" -Filter "NotoSerif*" -ErrorAction SilentlyContinue)) {
  Write-Host "WARNING: Noto Serif is not installed; Manim will fall back to another serif font (layout differs from the QA'd render)." -ForegroundColor Yellow
}

# ---------------------------------------------------------------- 2. engine (public repo, shallow, isolated venv)
$repo = Join-Path $Work "repo"
if (-not (Test-Path $repo)) { git clone --depth 1 https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize.git $repo }
$eng  = Join-Path $repo "pdf2video"
$venv = Join-Path $Work "venv"
if (-not (Test-Path $venv)) { python -m venv $venv }
$py = Join-Path $venv "Scripts\python.exe"
& $py -m pip install --upgrade pip | Out-Null
# Pillow is pinned here: Pillow 13 removed Image.fromarray(mode=...) which ManimCE 0.22 still uses,
# and pdfplumber needs Pillow >= 12.2.
& $py -m pip install -r (Join-Path $eng "requirements.txt") "pillow>=12.2,<13" psutil
& $py -m pip check

# ---------------------------------------------------------------- 3. engine tests
Push-Location $eng
& $py -m pytest -q -p no:cacheprovider tests
if ($LASTEXITCODE) { Pop-Location; Stop-Transcript | Out-Null; exit 20 }

# ---------------------------------------------------------------- 4. measured preview + final
$meter = Join-Path $repo "saas\bench\measure.py"     # present only on the SaaS branch; copy it next to this script if missing
if (-not (Test-Path $meter)) { $meter = Join-Path $PSScriptRoot "..\..\bench\measure.py" }
if (-not $Spec) { $Spec = Join-Path $eng "examples\physics\spec.json" }
$specDir = Split-Path $Spec -Parent
if ($Pdf) { Copy-Item $Pdf (Join-Path $specDir (Split-Path $Pdf -Leaf)) -Force -ErrorAction SilentlyContinue }

$out = Join-Path $Work "results"; New-Item -ItemType Directory -Force -Path $out | Out-Null
& $py -m pdf2video validate $Spec --name m1_validate
if ($LASTEXITCODE) { Pop-Location; Stop-Transcript | Out-Null; exit 30 }

& $py $meter --out (Join-Path $out "m1_preview_480p15.json") -- $py -m pdf2video render $Spec --name m1_prev --quality ql --fps 15 --problems 1
if ($SkipFinal) { Write-Host "SkipFinal: done." } else {
  & $py $meter --out (Join-Path $out "m1_final_1080p30.json") -- $py -m pdf2video run $Spec --name m1_final
}
Copy-Item (Join-Path $eng "build\m1_final\qa") (Join-Path $out "qa") -Recurse -Force -ErrorAction SilentlyContinue
Pop-Location
Write-Host "`nResults in $out   (m1_*.json = measured CPU/RAM/GPU; qa\ = engine QA, contact sheet, SHA256SUMS)"
Stop-Transcript | Out-Null

if ($Shutdown) {
  Write-Host "Shutting down in 60 s. Cancel with: shutdown /a" -ForegroundColor Yellow
  shutdown /s /t 60 /c "AniMotionPDF M1 finished"
}
