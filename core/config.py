"""
⚙️ Configuration Module
━━━━━━━━━━━━━━━━━━━━━━
Application configuration, colors, and constants
"""

import sys
import os
from dotenv import load_dotenv

# Handle PyInstaller exe - find the correct base path
if getattr(sys, 'frozen', False):
    # Running as exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script - go up one level from core/
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Change working directory to base dir (for .env and cache files)
os.chdir(BASE_DIR)

# Load .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Try to import optional dependencies
try:
    from colorthief import ColorThief
except ImportError:
    ColorThief = None

try:
    os.environ["QT_API"] = "pyside6"
    import qtawesome as qta
except ImportError:
    qta = None


class Colors:
    """Application color constants"""
    PRIMARY = "#1DB954"
    CARD = "#1a1a1a"
    HOVER = "#252525"
    TEXT = "#ffffff"
    TEXT_DIM = "#888888"
    ACCENT = "#2a2a2a"
    BORDER = "#333333"


class Config:
    """Application configuration constants"""
    COLLAPSED_W, COLLAPSED_H = 200, 52
    EXPANDED_W, EXPANDED_H = 480, 150
    ANIMATION_MS = 350
    POLL_FAST = 0.5      # When playing
    POLL_SLOW = 2.0      # When paused/idle
    CACHE_MAX = 50       # Max cached images/colors


# Spotify API credentials (loaded from .env)
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback")
SCOPE = "user-read-playback-state user-modify-playback-state user-library-modify user-library-read"
