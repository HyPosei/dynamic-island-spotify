"""
🎨 Widgets Module
━━━━━━━━━━━━━━━━
Custom Qt widgets for Dynamic Island UI
"""

from PySide6.QtWidgets import QWidget, QPushButton, QSlider
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QPainterPath, QCursor

from .config import Colors

# Try to import qtawesome
try:
    import qtawesome as qta
except ImportError:
    qta = None


class RoundedPanel(QWidget):
    """Custom widget with rounded corners and shadow"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bg_color = QColor(Colors.CARD)
        self.border_color = QColor(Colors.BORDER)
        self.corner_radius = 26
        self.setAttribute(Qt.WA_TranslucentBackground)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 
                           self.corner_radius, self.corner_radius)
        
        painter.fillPath(path, QBrush(self.bg_color))
        painter.setPen(QPen(self.border_color, 1))
        painter.drawPath(path)


class StyledButton(QPushButton):
    """Spotify-styled button with hover effects and optional qtawesome icon"""
    
    def __init__(self, icon_name, fallback_text, size=32, parent=None):
        super().__init__(parent)
        self.icon_name = icon_name
        self.fallback_text = fallback_text
        self.icon_color = "white"
        self.setFixedSize(size, size)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._update_icon()
        self._update_style()
        
    def _update_icon(self):
        if qta:
            # Color conversion for qtawesome
            c = self.icon_color
            if c == Colors.PRIMARY: c = "#1DB954"
            elif c == Colors.ACCENT: c = "#2a2a2a"
            
            try:
                self.setIcon(qta.icon("fa5s.circle", color="transparent"))
                icon = qta.icon(self.icon_name, color=c)
                self.setIcon(icon)
                self.setIconSize(self.size() * 0.6)
                self.setText("")
            except Exception:
                self.setIcon(qta.icon("fa5s.question", color=c))
                self.setText("")
        else:
            self.setText(self.fallback_text)
        self.update()
        self.repaint()
            
    def _update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: {self.width() // 2}px;
                color: {self.icon_color};
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            QPushButton:pressed {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
        """)
        
    def set_active(self, active, color=None):
        self._is_active = active
        self.icon_color = (color or Colors.PRIMARY) if active else "white"
        # Add subtle background when active
        if active and color:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 255, 255, 0.08);
                    border: none;
                    border-radius: {self.width() // 2}px;
                    color: {self.icon_color};
                    font-size: 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.15);
                }}
            """)
        else:
            self._update_style()
        self._update_icon()
    
    def set_color(self, color):
        """Set icon color directly without changing active state"""
        self.icon_color = color
        self._update_icon()
        self._update_style()
        
    def set_icon_state(self, icon_name, fallback_text):
        """Update icon/text for toggle states"""
        self.icon_name = icon_name
        self.fallback_text = fallback_text
        self._update_icon()
        self.repaint()


class StyledSlider(QSlider):
    """Spotify-styled slider"""
    
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.accent_color = Colors.PRIMARY
        self._update_style()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def _update_style(self):
        self.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: {Colors.ACCENT};
                height: 4px;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {self.accent_color};
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }}
            QSlider::sub-page:horizontal {{
                background: {self.accent_color};
                border-radius: 2px;
            }}
        """)
        
    def set_accent(self, color):
        self.accent_color = color
        self._update_style()
