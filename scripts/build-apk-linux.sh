#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Instalando dependencias del sistema (solo la primera vez tarda)..."
sudo apt-get update -qq
sudo apt-get install -y \
  python3-pip python3-venv \
  git zip unzip openjdk-17-jdk \
  autoconf automake libtool pkg-config \
  zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
  cmake libffi-dev libssl-dev \
  > /dev/null

echo "==> Instalando Buildozer..."
python3 -m pip install --user --upgrade pip setuptools wheel
python3 -m pip install --user "buildozer==1.5.0" "Cython==0.29.36"
export PATH="$HOME/.local/bin:$PATH"

echo "==> Compilando APK..."
buildozer android clean
buildozer -v android debug

echo ""
echo "==> Listo. APK en:"
ls -la bin/*.apk
