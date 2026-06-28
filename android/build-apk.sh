#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
mkdir -p bin docker-buildozer docker-gradle

docker build -t breakout-buildozer -f Dockerfile.buildozer ..
docker run --rm \
  -u "$(id -u):$(id -g)" \
  -v "$(pwd)/docker-buildozer:/home/user/.buildozer" \
  -v "$(pwd)/docker-gradle:/home/user/.gradle" \
  -v "$(pwd):/home/user/hostcwd" \
  breakout-buildozer -v android debug

echo ""
echo "APK generado en: $(pwd)/bin/"
