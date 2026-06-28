# Empaqueta los archivos del juego para copiarlos al telefono
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$files = @(
    "main.py",
    "game.py",
    "entities.py",
    "config.py",
    "platform_utils.py",
    "requirements.txt",
    "LEEME_ANDROID.txt"
)

$staging = Join-Path $env:TEMP "breakout-android-staging"
$zipPath = Join-Path $PSScriptRoot\.. "breakout-android.zip"

if (Test-Path $staging) { Remove-Item $staging -Recurse -Force }
New-Item -ItemType Directory -Path (Join-Path $staging "breakout") | Out-Null

foreach ($file in $files) {
    Copy-Item $file (Join-Path $staging "breakout\$file")
}

if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path (Join-Path $staging "breakout") -DestinationPath $zipPath -Force
Remove-Item $staging -Recurse -Force

Write-Host "Paquete listo:" -ForegroundColor Green
Write-Host "  $zipPath"
