"""
🎵 Dynamic Island Spotify Controller
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GPU-accelerated smooth animations with Qt6

Features:
- Adaptive color theming from album art
- Smooth expand/collapse animations
- Full playback control with shuffle & like
- Progress bar with seek
- Volume control with scroll wheel
"""

import sys
import os
import threading
from io import BytesIO

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, 
    QHBoxLayout, QVBoxLayout,
    QGraphicsDropShadowEffect, QSystemTrayIcon, QMenu
)
from PySide6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, 
    Signal, QRect, QSettings
)
from PySide6.QtGui import (
    QColor, QPainter, QBrush, QPen,
    QPixmap, QImage, QPainterPath, QIcon, QAction
)

import requests

# Import from core package
from core import (
    Colors, Config, BASE_DIR,
    SpotifyWorker,
    RoundedPanel, StyledButton, StyledSlider,
    SettingsDialog
)
from core.config import ColorThief, qta


# ══════════════════════════════════════════════════════════════
# MAIN DYNAMIC ISLAND WINDOW
# ══════════════════════════════════════════════════════════════

class DynamicIsland(QMainWindow):
    
    # Signals
    color_extracted = Signal(str)
    album_art_loaded = Signal(QImage)
    like_toggled = Signal()  # New signal for like button update
    
    # Caches (class-level)
    _image_cache = {}
    _color_cache = {}
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Settings for persistence
        self.settings = QSettings("DynamicIsland", "SpotifyController")
        
        # State
        self.is_expanded = False
        self.current_track_id = None
        self.accent_color = Colors.PRIMARY
        self.current_volume = 50
        self.track_duration = 1
        self._seeking = False
        self._volume_changing = False
        self._current_image_url = None
        self._is_liked = False
        self._is_shuffle = False
        self._is_repeat = 'off'
        
        # Load settings
        self.mini_mode = self.settings.value("mini_mode", False, type=bool)
        self.button_size = self.settings.value("button_size", 32, type=int)
        
        # Initial size
        self._current_w = Config.COLLAPSED_W
        self._current_h = Config.COLLAPSED_H
        self._load_position()
        
        # Build UI
        self._build_ui()
        
        # Animations
        self._setup_animations()
        
        # Connect signals
        self.color_extracted.connect(self._set_accent)
        self.album_art_loaded.connect(self._on_album_art_loaded)
        self.like_toggled.connect(self._update_like_button)
        
        # Spotify worker
        self.worker = SpotifyWorker()
        self.worker.track_updated.connect(self._on_track_update)
        self.worker.playback_updated.connect(self._on_playback_update)
        
        self.poll_thread = threading.Thread(target=self.worker.poll, daemon=True)
        self.poll_thread.start()
        
        # Mouse tracking
        self.setMouseTracking(True)
        
        # System tray
        self._setup_tray()
        
    def _load_position(self):
        """Load saved window position or center"""
        pos_x = self.settings.value("pos_x", None)
        pos_y = self.settings.value("pos_y", None)
        
        if pos_x is not None and pos_y is not None:
            self.setGeometry(int(pos_x), int(pos_y), self._current_w, self._current_h)
        else:
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - self._current_w) // 2
            self.setGeometry(x, 10, self._current_w, self._current_h)
            
    def _save_position(self):
        """Save window position"""
        self.settings.setValue("pos_x", self.x())
        self.settings.setValue("pos_y", self.y())
        
    def _setup_tray(self):
        """Setup system tray icon"""
        self.tray = QSystemTrayIcon(self)
        self.tray.setToolTip("Dynamic Island Spotify")
        
        # Create a programmatic icon (green circle with music note)
        icon_pixmap = QPixmap(32, 32)
        icon_pixmap.fill(Qt.transparent)
        painter = QPainter(icon_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(Colors.PRIMARY)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, 28, 28)
        painter.setPen(QPen(QColor("white")))
        painter.setFont(painter.font())
        painter.drawText(icon_pixmap.rect(), Qt.AlignCenter, "♪")
        painter.end()
        self.tray.setIcon(QIcon(icon_pixmap))
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        settings_action = QAction("⚙ Ayarlar / Settings", self)
        settings_action.triggered.connect(self._show_settings)
        tray_menu.addAction(settings_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self._quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray.setContextMenu(tray_menu)
        self.tray.activated.connect(self._tray_activated)
        self.tray.show()
        
    def _tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()
            
    def _quit_app(self):
        self._save_position()
        self.worker.stop()
        QApplication.quit()
        
    def _show_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self)
        dialog.exec()
        
    def _build_ui(self):
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main panel
        self.panel = RoundedPanel(central)
        self.panel.setGeometry(0, 0, self._current_w, self._current_h)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 4)
        self.panel.setGraphicsEffect(shadow)
        
        # Layout
        self.layout = QVBoxLayout(self.panel)
        self.layout.setContentsMargins(12, 8, 12, 8)
        self.layout.setSpacing(6)
        
        # Top row (always visible)
        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        
        # Album art
        self.album_art = QLabel()
        self.album_art.setFixedSize(36, 36)
        self.album_art.setStyleSheet(f"""
            background-color: {Colors.ACCENT};
            border-radius: 8px;
            color: white;
            font-size: 16px;
        """)
        self.album_art.setAlignment(Qt.AlignCenter)
        self.album_art.setText("♪")
        self.album_art.mousePressEvent = lambda e: self._open_spotify()
        top_row.addWidget(self.album_art)
        
        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        self.title_label = QLabel("Not Playing")
        self.title_label.setStyleSheet(f"color: {Colors.TEXT}; font-size: 13px; font-weight: bold;")
        self.title_label.setMaximumWidth(100)
        
        self.artist_label = QLabel("Open Spotify")
        self.artist_label.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 11px;")
        self.artist_label.setMaximumWidth(100)
        
        info_layout.addWidget(self.title_label)
        info_layout.addWidget(self.artist_label)
        top_row.addLayout(info_layout)
        
        top_row.addStretch()
        
        # Volume indicator (collapsed)
        self.vol_indicator = QLabel("🔊")
        self.vol_indicator.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 12px;")
        top_row.addWidget(self.vol_indicator)
        
        # Control buttons (expanded)
        self.controls = QWidget()
        controls_layout = QHBoxLayout(self.controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(4)
        
        # New buttons: Shuffle, Like
        bs = self.button_size  # Base button size
        self.btn_shuffle = StyledButton("fa5s.random", "⇌", bs)
        self.btn_like = StyledButton("mdi.heart-outline", "♡", bs)
        self.btn_repeat = StyledButton("fa5s.redo", "↻", bs)
        self.btn_prev = StyledButton("fa5s.step-backward", "◀◀", bs + 2)
        self.btn_play = StyledButton("fa5s.play", "▶", bs + 10)
        self.btn_next = StyledButton("fa5s.step-forward", "▶▶", bs + 2)
        self.btn_close = StyledButton("fa5s.times", "×", bs - 4)
        
        self.btn_shuffle.clicked.connect(self._toggle_shuffle)
        self.btn_like.clicked.connect(self._toggle_like)
        self.btn_repeat.clicked.connect(self._toggle_repeat)
        self.btn_prev.clicked.connect(self._prev_track)
        self.btn_play.clicked.connect(self._toggle_play)
        self.btn_next.clicked.connect(self._next_track)
        self.btn_close.clicked.connect(self._quit_app)
        
        controls_layout.addWidget(self.btn_shuffle)
        controls_layout.addWidget(self.btn_like)
        controls_layout.addWidget(self.btn_prev)
        controls_layout.addWidget(self.btn_play)
        controls_layout.addWidget(self.btn_next)
        controls_layout.addWidget(self.btn_repeat)
        controls_layout.addWidget(self.btn_close)
        
        self.controls.hide()
        top_row.addWidget(self.controls)
        
        self.layout.addLayout(top_row)
        
        # Seek bar (expanded)
        self.seek_row = QWidget()
        seek_layout = QHBoxLayout(self.seek_row)
        seek_layout.setContentsMargins(0, 0, 0, 0)
        seek_layout.setSpacing(8)
        
        self.time_current = QLabel("0:00")
        self.time_current.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 10px;")
        
        self.seek_slider = StyledSlider()
        self.seek_slider.setRange(0, 100)
        self.seek_slider.sliderPressed.connect(lambda: setattr(self, '_seeking', True))
        self.seek_slider.sliderReleased.connect(self._on_seek_release)
        
        self.time_total = QLabel("0:00")
        self.time_total.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 10px;")
        
        seek_layout.addWidget(self.time_current)
        seek_layout.addWidget(self.seek_slider)
        seek_layout.addWidget(self.time_total)
        
        self.seek_row.hide()
        self.layout.addWidget(self.seek_row)
        
        # Volume slider (expanded)
        self.vol_slider = StyledSlider()
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(50)
        self.vol_slider.valueChanged.connect(self._on_volume_change)
        self.vol_slider.hide()
        self.layout.addWidget(self.vol_slider)
        
    def _setup_animations(self):
        self.size_anim = QPropertyAnimation(self, b"geometry")
        self.size_anim.setEasingCurve(QEasingCurve.OutBack)
        self.size_anim.setDuration(Config.ANIMATION_MS)
        
    def enterEvent(self, event):
        self._expand()
        
    def leaveEvent(self, event):
        self._collapse()
        
    def _expand(self):
        if self.is_expanded or self.mini_mode:
            return
        self.is_expanded = True
        
        self.vol_indicator.hide()
        self.controls.show()
        self.seek_row.show()
        self.vol_slider.show()
        self.album_art.setFixedSize(48, 48)
        self.title_label.setMaximumWidth(200)
        self.artist_label.setMaximumWidth(200)
        
        QTimer.singleShot(10, self._apply_album_art)
        
        current_x = self.x()
        current_y = self.y()
        new_x = current_x - (Config.EXPANDED_W - self._current_w) // 2
        
        self.size_anim.setStartValue(self.geometry())
        self.size_anim.setEndValue(QRect(new_x, current_y, Config.EXPANDED_W, Config.EXPANDED_H))
        self.size_anim.start()
        
        self._current_w = Config.EXPANDED_W
        self._current_h = Config.EXPANDED_H
        
    def _collapse(self):
        if not self.is_expanded:
            return
        self.is_expanded = False
        
        self.controls.hide()
        self.seek_row.hide()
        self.vol_slider.hide()
        self.vol_indicator.show()
        self.album_art.setFixedSize(36, 36)
        self.title_label.setMaximumWidth(100)
        self.artist_label.setMaximumWidth(100)
        
        QTimer.singleShot(10, self._apply_album_art)
        
        current_x = self.x()
        current_y = self.y()
        new_x = current_x + (self._current_w - Config.COLLAPSED_W) // 2
        
        self.size_anim.setStartValue(self.geometry())
        self.size_anim.setEndValue(QRect(new_x, current_y, Config.COLLAPSED_W, Config.COLLAPSED_H))
        self.size_anim.start()
        
        self._current_w = Config.COLLAPSED_W
        self._current_h = Config.COLLAPSED_H
        
    def resizeEvent(self, event):
        self.panel.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, '_drag_pos'):
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            
    def mouseReleaseEvent(self, event):
        if hasattr(self, '_drag_pos'):
            del self._drag_pos
            self._save_position()
        
    def _on_track_update(self, data):
        if not data:
            self.title_label.setText("Not Playing")
            self.artist_label.setText("Open Spotify")
            self.btn_play.set_icon_state("fa5s.play", "▶")
            self.album_art.setText("♪")
            self.album_art.setPixmap(QPixmap())
            self._set_accent(Colors.PRIMARY)
            self.current_track_id = None
            return
            
        track = data['item']
        self.current_track_id = track['id']
        track_name = track['name'][:25] + "..." if len(track['name']) > 25 else track['name']
        self.title_label.setText(track_name)
        self.artist_label.setText(track['artists'][0]['name'][:20])
        
        # Check if track is liked
        threading.Thread(target=self._check_liked, daemon=True).start()
        
        # Load album art
        images = track['album'].get('images', [])
        if images:
            small_img = images[-1] if len(images) > 1 else images[0]
            img_url = small_img['url']
            
            if img_url == self._current_image_url:
                return
            self._current_image_url = img_url
            
            if img_url in DynamicIsland._image_cache:
                self._original_album_pixmap = DynamicIsland._image_cache[img_url]
                QTimer.singleShot(0, self._apply_album_art)
                if img_url in DynamicIsland._color_cache:
                    cached_color = DynamicIsland._color_cache[img_url]
                    QTimer.singleShot(0, lambda c=cached_color: self._set_accent(c))
                else:
                    threading.Thread(target=self._extract_color_only, args=(img_url,), daemon=True).start()
            else:
                threading.Thread(target=self._load_album_art, args=(img_url,), daemon=True).start()
                
    def _check_liked(self):
        """Check if current track is liked"""
        if self.current_track_id:
            self._is_liked = self.worker.is_liked(self.current_track_id)
            QTimer.singleShot(0, self._update_like_button)
            
    def _update_like_button(self):
        if self._is_liked:
            # Solid filled heart when liked
            self.btn_like.set_icon_state("mdi.heart", "❤")
            self.btn_like.set_active(True, self.accent_color)
        else:
            # Outline heart when not liked
            self.btn_like.set_icon_state("mdi.heart-outline", "♡")
            self.btn_like.set_color(self.accent_color)
            
    def _on_playback_update(self, data):
        if not data:
            return
            
        is_playing = data.get('is_playing', False)
        if is_playing:
            self.btn_play.set_icon_state("fa5s.pause", "❚❚")
        else:
            self.btn_play.set_icon_state("fa5s.play", "▶")
        
        # Shuffle state - use accent color
        self._is_shuffle = data.get('shuffle_state', False)
        if self._is_shuffle:
            self.btn_shuffle.set_active(True, self.accent_color)
        else:
            self.btn_shuffle.set_color(self.accent_color)  # Use accent color even when inactive
        
        # Repeat state - use accent color
        self._is_repeat = data.get('repeat_state', 'off')
        if self._is_repeat == 'context':
            # Context repeat (All) - infinity symbol
            self.btn_repeat.set_icon_state("fa5s.redo", "∞")
            self.btn_repeat.set_active(True, self.accent_color)
        elif self._is_repeat == 'track':
            # Track repeat (One) - "1" with circle
            self.btn_repeat.set_icon_state("fa5s.sync", "¹↻")
            self.btn_repeat.set_active(True, self.accent_color)
        else:
            # Repeat off
            self.btn_repeat.set_icon_state("fa5s.redo", "↻")
            self.btn_repeat.set_color(self.accent_color)  # Use accent color even when inactive
            
        # Volume
        device = data.get('device', {})
        vol = device.get('volume_percent', 50)
        self.current_volume = vol
        if not self._volume_changing:
            self.vol_slider.blockSignals(True)
            self.vol_slider.setValue(vol)
            self.vol_slider.blockSignals(False)
            self._update_vol_icon(vol)
            
        # Progress
        item = data.get('item', {})
        duration = item.get('duration_ms', 1)
        progress = data.get('progress_ms', 0)
        self.track_duration = duration
        
        if not self._seeking:
            pct = int((progress / duration) * 100) if duration > 0 else 0
            self.seek_slider.blockSignals(True)
            self.seek_slider.setValue(pct)
            self.seek_slider.blockSignals(False)
            self._update_times(progress, duration)
            
    def _load_album_art(self, url):
        try:
            response = requests.get(url, timeout=10)
            img_data = response.content
            
            if ColorThief:
                try:
                    thief = ColorThief(BytesIO(img_data))
                    # Get dominant color directly
                    r, g, b = thief.get_color(quality=1)
                    
                    # Ensure color is not too dark (since bg is dark)
                    brightness = (r + g + b) / 3
                    if brightness < 60:
                        # Brighten the color
                        factor = 1.5
                        r = min(255, int(r * factor))
                        g = min(255, int(g * factor))
                        b = min(255, int(b * factor))
                        
                        # If still too dark, fallback to primary or boost more
                        if (r + g + b) / 3 < 60:
                            # Use a lighter version of the color
                            r, g, b = [min(255, c + 60) for c in (r, g, b)]
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    # Cache with limit
                    DynamicIsland._color_cache[url] = color
                    if len(DynamicIsland._color_cache) > Config.CACHE_MAX:
                        oldest = next(iter(DynamicIsland._color_cache))
                        del DynamicIsland._color_cache[oldest]
                        
                    self.color_extracted.emit(color)
                except Exception as e:
                    print(f"Color extraction error: {e}")
                    self.color_extracted.emit(Colors.PRIMARY)
            else:
                print("ColorThief not installed, using default color")
                self.color_extracted.emit(Colors.PRIMARY)
                
            from PySide6.QtCore import QByteArray
            byte_array = QByteArray(img_data)
            qimg = QImage()
            if qimg.loadFromData(byte_array):
                self.album_art_loaded.emit(qimg)
        except Exception as e:
            print(f"Image load error: {e}")
            
    def _on_album_art_loaded(self, image):
        """Handle loaded album art image (Main Thread)"""
        pixmap = QPixmap.fromImage(image)
        self._original_album_pixmap = pixmap
        
        # Re-implement cache logic properly:
        if self._current_image_url:
            DynamicIsland._image_cache[self._current_image_url] = pixmap
            if len(DynamicIsland._image_cache) > Config.CACHE_MAX:
                oldest = next(iter(DynamicIsland._image_cache))
                del DynamicIsland._image_cache[oldest]
            
        self._apply_album_art()
            
    def _extract_color_only(self, url):
        try:
            if ColorThief:
                response = requests.get(url, timeout=10)
                thief = ColorThief(BytesIO(response.content))
                # Get dominant color directly
                r, g, b = thief.get_color(quality=1)
                
                # Ensure color is not too dark
                brightness = (r + g + b) / 3
                if brightness < 60:
                    factor = 1.5
                    r = min(255, int(r * factor))
                    g = min(255, int(g * factor))
                    b = min(255, int(b * factor))
                    
                    if (r + g + b) / 3 < 60:
                         r, g, b = [min(255, c + 60) for c in (r, g, b)]
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                DynamicIsland._color_cache[url] = color
                self.color_extracted.emit(color)
            else:
                self.color_extracted.emit(Colors.PRIMARY)
        except Exception as e:
            print(f"Color extract only error: {e}")
            self.color_extracted.emit(Colors.PRIMARY)
            
    def _create_rounded_pixmap(self, pixmap, size, radius):
        scaled = pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        
        if scaled.width() != size or scaled.height() != size:
            x = (scaled.width() - size) // 2
            y = (scaled.height() - size) // 2
            scaled = scaled.copy(x, y, size, size)
        
        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)
        
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, size, size, radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled)
        painter.end()
        
        return rounded
            
    def _apply_album_art(self):
        pixmap = getattr(self, '_original_album_pixmap', None)
        if pixmap and not pixmap.isNull():
            size = self.album_art.width()
            rounded = self._create_rounded_pixmap(pixmap, size, 8)
            self.album_art.setPixmap(rounded)
            self.album_art.setText("")
            self.album_art.setScaledContents(False)

    def _set_accent(self, color):
        self.accent_color = color
        
        # Play button background remains transparent, maybe update icon color if needed?
        # For now, keeping it white on transparent background
        
        # Update sliders
        self.seek_slider.set_accent(color)
        self.vol_slider.set_accent(color)
        
        # Force update ALL buttons with new accent color (for active states)
        self._refresh_button_colors()
        
    def _refresh_button_colors(self):
        """Refresh all button colors with current accent color"""
        color = self.accent_color
        
        # Shuffle button - always use accent color
        if self._is_shuffle:
            self.btn_shuffle.set_active(True, color)
        else:
            self.btn_shuffle.set_color(color)
            
        # Like button
        if self._is_liked:
            self.btn_like.set_active(True, color)
        else:
            self.btn_like.set_color(color)
            
        # Repeat button
        if hasattr(self, '_is_repeat') and self._is_repeat != 'off':
            self.btn_repeat.set_active(True, color)
        else:
            self.btn_repeat.set_color(color)
        
        # Control buttons - always use accent color
        self.btn_prev.set_color(color)
        self.btn_play.set_color(color)
        self.btn_next.set_color(color)
        
    def _apply_button_size(self, size):
        """Apply new button size to all buttons"""
        self.button_size = size
        self.btn_shuffle.setFixedSize(size, size)
        self.btn_like.setFixedSize(size, size)
        self.btn_repeat.setFixedSize(size, size)
        self.btn_prev.setFixedSize(size + 2, size + 2)
        self.btn_play.setFixedSize(size + 10, size + 10)
        self.btn_next.setFixedSize(size + 2, size + 2)
        self.btn_close.setFixedSize(size - 4, size - 4)
        # Refresh icons with new size
        self._refresh_button_colors()
                
    def _update_vol_icon(self, vol):
        icon = "🔇" if vol == 0 else "🔈" if vol < 33 else "🔉" if vol < 66 else "🔊"
        self.vol_indicator.setText(icon)
        
    def _update_times(self, current_ms, total_ms):
        def fmt(ms):
            s = ms // 1000
            return f"{s//60}:{s%60:02d}"
        self.time_current.setText(fmt(current_ms))
        self.time_total.setText(fmt(total_ms))
        
    # ──────────────────────────────────────────────────────────
    # CONTROLS
    # ──────────────────────────────────────────────────────────
    
    def _toggle_play(self):
        def action():
            try:
                state = self.worker.sp.current_playback()
                if state and state.get('is_playing'):
                    self.worker.sp.pause_playback()
                else:
                    self.worker.sp.start_playback()
            except: pass
        threading.Thread(target=action, daemon=True).start()
        
    def _next_track(self):
        threading.Thread(target=lambda: self.worker.sp.next_track(), daemon=True).start()
        
    def _prev_track(self):
        threading.Thread(target=lambda: self.worker.sp.previous_track(), daemon=True).start()
        
    def _toggle_shuffle(self):
        def action():
            try:
                new_state = not self._is_shuffle
                self.worker.sp.shuffle(new_state)
            except Exception as e:
                # Handle 403 errors (Premium required, podcasts, etc.)
                # Silently ignore restriction violations
                pass
        threading.Thread(target=action, daemon=True).start()
        
    def _toggle_like(self):
        def action():
            if self.current_track_id:
                result = self.worker.toggle_like(self.current_track_id)
                if result is not None:
                    self._is_liked = result
                    self.like_toggled.emit()
        threading.Thread(target=action, daemon=True).start()
        
    def _toggle_repeat(self):
        def action():
            try:
                state = self.worker.sp.current_playback()
                if not state: return
                current = state.get('repeat_state', 'off')
                new = {'off': 'context', 'context': 'track', 'track': 'off'}[current]
                self.worker.sp.repeat(new)
            except: pass
        threading.Thread(target=action, daemon=True).start()
        
    def _on_seek_release(self):
        self._seeking = False
        val = self.seek_slider.value()
        pos_ms = int((val / 100) * self.track_duration)
        threading.Thread(target=lambda: self.worker.sp.seek_track(pos_ms), daemon=True).start()
        
    def _on_volume_change(self, val):
        self._volume_changing = True
        self.current_volume = val
        self._update_vol_icon(val)
        
        if hasattr(self, '_vol_timer'):
            self._vol_timer.stop()
        self._vol_timer = QTimer()
        self._vol_timer.setSingleShot(True)
        self._vol_timer.timeout.connect(lambda: self._set_volume(val))
        self._vol_timer.start(150)
        
    def _set_volume(self, vol):
        self._volume_changing = False
        threading.Thread(target=lambda: self.worker.sp.volume(vol), daemon=True).start()
        
    def _open_spotify(self):
        if sys.platform == 'win32':
            os.startfile("spotify")
        elif sys.platform == 'darwin':
            os.system("open -a Spotify")
        else:
            os.system("spotify &")
        self._expand()
        
    def wheelEvent(self, event):
        delta = 5 if event.angleDelta().y() > 0 else -5
        new_vol = max(0, min(100, self.current_volume + delta))
        self.vol_slider.setValue(new_vol)
        
    def closeEvent(self, event):
        self._save_position()
        self.worker.stop()
        event.accept()


# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if not ColorThief:
        print("⚠️  Install colorthief for dynamic colors: pip install colorthief")
        
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setQuitOnLastWindowClosed(False)  # Keep running in tray
    
    window = DynamicIsland()
    window.show()
    
    sys.exit(app.exec())