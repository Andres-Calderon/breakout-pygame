# Compilar Breakout a .exe (Windows)
# Uso: .\build.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Instalando dependencias de compilacion..." -ForegroundColor Cyan
pip install -r requirements-build.txt

Write-Host "Compilando ejecutable..." -ForegroundColor Cyan
pyinstaller `
    --noconfirm `
    --onefile `
    --windowed `
    --name "Breakout" `
    --collect-all pygame `
    main.py

Write-Host ""
Write-Host "Listo. Ejecutable en:" -ForegroundColor Green
Write-Host "  $PSScriptRoot\dist\Breakout.exe"
