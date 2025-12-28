"""
🎧 Spotify Worker Module
━━━━━━━━━━━━━━━━━━━━━━━
Background thread for Spotify API calls with adaptive polling
"""

import time
import os

from PySide6.QtCore import Signal, QObject
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .config import (
    BASE_DIR, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE, Config
)


class SpotifyWorker(QObject):
    """Background thread for Spotify API calls with adaptive polling"""
    track_updated = Signal(dict)
    playback_updated = Signal(dict)
    error = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.sp = None
        self._is_playing = False
        self._init_spotify()
        
    def _init_spotify(self):
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI,
                scope=SCOPE,
                cache_path=os.path.join(BASE_DIR, ".spotify_cache")
            ))
        except Exception as e:
            self.error.emit(str(e))
            
    def poll(self):
        last_track_id = None
        while self.running:
            if self.sp:
                try:
                    playback = self.sp.current_playback()
                    if playback and playback.get('item'):
                        self._is_playing = playback.get('is_playing', False)
                        self.playback_updated.emit(playback)
                        
                        track_id = playback['item']['id']
                        if track_id != last_track_id:
                            last_track_id = track_id
                            self.track_updated.emit(playback)
                    else:
                        self._is_playing = False
                        if last_track_id:
                            last_track_id = None
                            self.track_updated.emit({})
                except Exception as e:
                    if "expired" in str(e).lower():
                        self._init_spotify()
            
            # Adaptive polling - faster when playing
            sleep_time = Config.POLL_FAST if self._is_playing else Config.POLL_SLOW
            time.sleep(sleep_time)
            
    def stop(self):
        self.running = False
        
    def toggle_like(self, track_id):
        """Toggle like status for a track"""
        try:
            is_saved = self.sp.current_user_saved_tracks_contains([track_id])[0]
            if is_saved:
                self.sp.current_user_saved_tracks_delete([track_id])
                return False
            else:
                self.sp.current_user_saved_tracks_add([track_id])
                return True
        except Exception as e:
            print(f"Like toggle error: {e}")
            return None
            
    def is_liked(self, track_id):
        """Check if track is liked"""
        try:
            result = self.sp.current_user_saved_tracks_contains([track_id])
            return result[0] if result else False
        except Exception as e:
            print(f"Check liked error: {e}")
            return False
