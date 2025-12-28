"""
🎵 Dynamic Island Core Package
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Modular components for Dynamic Island Spotify Controller
"""

from .config import Colors, Config, BASE_DIR, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE
from .spotify_worker import SpotifyWorker
from .widgets import RoundedPanel, StyledButton, StyledSlider
from .settings import SettingsDialog

__all__ = [
    'Colors', 'Config', 'BASE_DIR',
    'CLIENT_ID', 'CLIENT_SECRET', 'REDIRECT_URI', 'SCOPE',
    'SpotifyWorker',
    'RoundedPanel', 'StyledButton', 'StyledSlider',
    'SettingsDialog'
]
