# Ejecuta tests del API y del adaptador (sin llamadas a Claude API, sin render).
$Root = Split-Path $PSScriptRoot -Parent; Set-Location $Root
$env:P2V_ENGINE_ROOT = Join-Path $Root "engine\pdf2video"
& (Join-Path $Root ".venv\Scripts\python.exe") -m pytest
