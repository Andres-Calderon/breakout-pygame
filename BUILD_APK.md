# Compilar Breakout como APK (Android)

Pygame no genera APK en Windows directamente. Necesitas **Linux** (WSL) o **GitHub Actions**.

---

## Opcion A: WSL en tu PC (recomendada si tienes tiempo)

### 1. Instalar WSL (una sola vez)

Abre **PowerShell como Administrador** y ejecuta:

```powershell
wsl --install -d Ubuntu
```

Reinicia el PC cuando termine. Abre **Ubuntu** desde el menu Inicio y crea tu usuario.

### 2. Compilar el APK

Doble clic en:

```
scripts\build-apk-wsl.bat
```

O en Ubuntu (WSL):

```bash
cd /mnt/c/Users/Zuge/Projects/breakout-pygame
chmod +x scripts/build-apk-linux.sh
./scripts/build-apk-linux.sh
```

La **primera compilacion** tarda 30-90 minutos (descarga SDK, NDK, compila Python y Pygame).

### 3. Instalar en el telefono

El APK queda en:

```
breakout-pygame\bin\breakout-1.0.0-arm64-v8a-debug.apk
```

Copialo al telefono e instalalo. Activa **"Origenes desconocidas"** si Android lo pide.

---

## Opcion B: GitHub Actions (sin instalar Linux)

Si tienes cuenta de GitHub:

1. Crea un repositorio y sube la carpeta `breakout-pygame`.
2. En GitHub: pestaña **Actions** → workflow **Build Android APK** → **Run workflow**.
3. Espera ~30-90 min.
4. Descarga el APK desde **Artifacts** (`breakout-apk`).

---

## Controles en el APK

- Toca para iniciar / lanzar pelota
- Arrastra el dedo para mover la barra
- Juega en horizontal

---

## Si falla la compilacion

Errores comunes:

| Error | Solucion |
|-------|----------|
| `No module named 'buildozer'` | Ejecuta `pip install buildozer` en WSL |
| Licencia SDK | Ya esta `android.accept_sdk_license = True` en buildozer.spec |
| pygame-ce falla | Revisa que exista `p4a-recipes/pygame-ce/__init__.py` |
| WSL no instalado | `wsl --install -d Ubuntu` y reinicia |

Para la entrega academica documenta:
- Herramienta: **Buildozer + python-for-android**
- Motor grafico: **pygame-ce** (fork de Pygame para movil)
- Resultado: archivo `.apk` instalable
