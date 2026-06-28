@echo off
echo ============================================
echo  Compilar Breakout APK con WSL + Buildozer
echo ============================================
echo.

wsl --status >nul 2>&1
if errorlevel 1 (
    echo WSL no esta instalado.
    echo.
    echo Instalalo con este comando en PowerShell COMO ADMINISTRADOR:
    echo   wsl --install -d Ubuntu
    echo.
    echo Luego reinicia el PC y vuelve a ejecutar este script.
    pause
    exit /b 1
)

echo Iniciando compilacion en Ubuntu (puede tardar 30-90 min la primera vez)...
echo.

wsl -d Ubuntu -e bash -lc "cd '/mnt/c/Users/Zuge/Projects/breakout-pygame' && chmod +x scripts/build-apk-linux.sh && ./scripts/build-apk-linux.sh"

if errorlevel 1 (
    echo.
    echo La compilacion fallo. Revisa los mensajes de arriba.
    pause
    exit /b 1
)

echo.
echo APK generado en: bin\breakout-*.apk
pause
