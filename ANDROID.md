# Breakout en Android

Pygame **no genera APK de forma nativa en Windows** de manera sencilla. Para tu proyecto académico hay **dos caminos**:


| Método                         | Dificultad | Resultado                       |
| ------------------------------ | ---------- | ------------------------------- |
| **A. Pydroid 3** (recomendado) | Baja       | Juego en el teléfono o emulador |
| **B. Buildozer + Docker**      | Alta       | APK instalable (.apk)           |


---

## Método A: Pydroid 3 (recomendado)

Es la forma más rápida de cumplir el requisito *"ejecutar en Android"* sin pelearte con compilación cruzada.

### En tu teléfono Android

1. Instala **[Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3)** desde Play Store.
2. En tu PC, genera el paquete del juego:

   **Opción fácil (CMD o doble clic):**
   ```cmd
   cd C:\Users\Zuge\Projects\breakout-pygame\scripts
   prepare_android_bundle.bat
   ```

   **O desde PowerShell sin cambiar políticas del sistema:**
   ```powershell
   cd C:\Users\Zuge\Projects\breakout-pygame
   powershell -ExecutionPolicy Bypass -File .\scripts\prepare_android_bundle.ps1
   ```

   Se crea `breakout-android.zip` en la carpeta del proyecto.
3. Envía el ZIP a tu teléfono (USB, WhatsApp, Drive, correo, etc.).
4. Descomprime el ZIP en el teléfono (carpeta `breakout`).
5. En Pydroid 3:
  - Menú **⋮ → Pip** → instala `pygame`
  - **Open** → navega a la carpeta `breakout` → abre `main.py`
  - Pulsa el botón **▶ Run**

### Controles en móvil

- **Tocar** → iniciar / lanzar pelota / reintentar
- **Arrastrar el dedo** → mover la barra
- Gira el teléfono en **horizontal** para jugar más cómodo

### En emulador Android (Android Studio)

1. Instala [Android Studio](https://developer.android.com/studio).
2. Crea un dispositivo virtual: **Device Manager → Create Virtual Device** (ej. Pixel 6).
3. Inicia el emulador.
4. Abre Play Store en el emulador e instala **Pydroid 3**.
5. Arrastra `breakout-android.zip` al emulador o usa ADB:
  ```powershell
   adb push breakout-android.zip /sdcard/Download/
  ```
6. Descomprime en el emulador con la app **Archivos** y sigue los pasos de Pydroid 3.

### Qué documentar en tu informe

- Herramienta: **Pydroid 3** (intérprete Python + Pygame en Android)
- Limitación: no es un APK compilado, pero **sí ejecuta el juego en Android**
- Ventaja: mismo código Python que en Windows

---

## Método B: Generar APK con Buildozer (avanzado)

Para un **APK real** necesitas **Linux** (WSL2 en Windows o una máquina virtual).

### Requisitos

- Windows con **WSL2** (Ubuntu) o Linux nativo
- **Docker** instalado
- ~5 GB de espacio libre
- Primera compilación: **30–90 minutos**

### Pasos resumidos (WSL2)

```bash
# Dentro de Ubuntu (WSL)
sudo apt update
sudo apt install -y docker.io git
sudo usermod -aG docker $USER
# Cierra y vuelve a abrir la terminal

cd /mnt/c/Users/Zuge/Projects/breakout-pygame/android
docker build -t breakout-buildozer -f Dockerfile.buildozer ..
docker run --rm -v "$(pwd):/home/user/hostcwd" breakout-buildozer android debug
```

El APK quedará en `android/bin/`.

> **Nota:** La receta de Pygame para Android es inestable. Si falla la compilación, usa el **Método A** para la entrega y menciona en el informe que intentaste Buildozer.

---

## Archivos adaptados para Android

- `platform_utils.py` — detecta Android y escala la pantalla
- `game.py` — controles táctiles (toque y arrastre)
- Fuentes del sistema en móvil (Consolas no existe en Android)

---

## Checklist de entrega

- [x] Juego funciona en Windows (`python main.py`)
- [x] Ejecutable `.exe` funciona (`dist\Breakout.exe`)
- [ ] Juego funciona en Android (Pydroid 3 o APK)
- [ ] Capturas de pantalla del juego en móvil/emulador
- [ ] Breve explicación de cada método de despliegue