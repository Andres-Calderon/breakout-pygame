[app]
title = Breakout
package.name = breakout
package.domain = org.estudiante.breakout
source.dir = .
source.include_exts = py
source.exclude_dirs = build, dist, android, scripts, .buildozer, bin, .git, .github
version = 1.0.0
requirements = python3==3.10.12,hostpython3==3.10.12,cython==0.29.36,setuptools==69.5.1,pygame-ce,sdl2,sdl2_image,sdl2_mixer,sdl2_ttf
orientation = landscape
fullscreen = 1
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.permissions = INTERNET
android.archs = arm64-v8a
android.accept_sdk_license = True
p4a.bootstrap = sdl2
p4a.local_recipes = ./p4a-recipes

[buildozer]
log_level = 2
warn_on_root = 1
