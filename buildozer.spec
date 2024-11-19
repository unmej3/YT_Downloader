[app]
# Title of your application (displayed to users)
title = YT_Downloader

# Package name (unique identifier, e.g., "com.company.myapp")
package.name = yt_downloader

# Package domain (reverse domain name style; can be any valid identifier)
package.domain = org.yt

# Source code directory where the `main.py` file resides
source.dir = .

# Source files to include (keep all relevant file extensions here)
source.include_exts = py,png,jpg,kv,atlas

# List of inclusions using pattern matching (include specific assets or directories)
# source.include_patterns = assets/*,images/*.png

# Source files or directories to exclude (e.g., tests, virtual environment, or unnecessary files)
source.exclude_exts = spec
source.exclude_dirs = tests, bin, venv

# Main Python file entry point for your app
# Default: main.py (update if your main script has a different name)
main = main.py

# (str) Icon of the application (must be a PNG file, optional but recommended)
icon.filename = assets/icon.png

# (str) Presplash screen image (optional, shown while app loads)
presplash.filename = assets/logo.png

# Permissions required for the app (e.g., Internet access, storage access)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Application version
version = 1.0

# Minimum Android API level (use 21 for better compatibility with modern devices)
android.minapi = 21

# Android SDK target (use 30 or 31 for modern compatibility)
android.api = 31

# Fullscreen mode (0: no, 1: yes)
fullscreen = 1

# Orientation of the app (portrait, landscape, or sensor for dynamic)
orientation = portrait

# Supported platforms for packaging
osx.kivy_version = 2.1.0
requirements = python3, kivy, yt-dlp

# (str) Additional Java code (optional)
# android.add_src = src

# Include ARM architectures for wider compatibility
android.archs = armeabi-v7a, arm64-v8a
