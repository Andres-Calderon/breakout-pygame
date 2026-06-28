import os
import sys


def is_android() -> bool:
    return "android" in sys.platform or "ANDROID_ARGUMENT" in os.environ


def is_mobile() -> bool:
    return is_android()


def configure_for_android() -> None:
    """Debe llamarse antes de importar pygame en Android."""
    if not is_android():
        return

    os.environ.setdefault("SDL_ANDROID_BLOCK_ON_PAUSE", "0")
    os.environ.setdefault("SDL_MOUSE_TOUCH_EVENTS", "1")
    os.environ.setdefault("SDL_VIDEO_ALLOW_SCREENSAVER", "1")


def setup_window():
    import pygame

    pygame.display.init()
    size = (800, 600)

    if is_mobile():
        # En Android/Pydroid, SCALED y RESIZABLE pueden romper SDL.
        return pygame.display.set_mode(size)

    return pygame.display.set_mode(size)
