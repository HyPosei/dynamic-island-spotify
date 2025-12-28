"""
⚙️ Settings Dialog Module
━━━━━━━━━━━━━━━━━━━━━━━━
Settings dialog for app configuration
"""

import sys
import os

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
    QCheckBox, QPushButton, QApplication, QSlider, QLabel
)
from PySide6.QtCore import Qt

from .config import Colors, Config


class SettingsDialog(QDialog):
    """Settings dialog for app configuration"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("Ayarlar / Settings")
        self.setFixedSize(380, 420)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.CARD};
                color: {Colors.TEXT};
            }}
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QCheckBox {{
                color: {Colors.TEXT};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid {Colors.BORDER};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Colors.PRIMARY};
                border-color: {Colors.PRIMARY};
            }}
            QSlider::groove:horizontal {{
                background: {Colors.ACCENT};
                height: 4px;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {Colors.PRIMARY};
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }}
            QSlider::sub-page:horizontal {{
                background: {Colors.PRIMARY};
                border-radius: 2px;
            }}
            QLabel {{
                color: {Colors.TEXT};
            }}
            QPushButton {{
                background-color: {Colors.PRIMARY};
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1ed760;
            }}
        """)
        
        self._build_ui()
        self._load_settings()
        
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # Startup group
        startup_group = QGroupBox("Başlangıç / Startup")
        startup_layout = QVBoxLayout(startup_group)
        
        self.startup_check = QCheckBox("Windows ile başlat / Start with Windows")
        startup_layout.addWidget(self.startup_check)
        
        layout.addWidget(startup_group)
        
        # Appearance group
        appearance_group = QGroupBox("Görünüm / Appearance")
        appearance_layout = QVBoxLayout(appearance_group)
        
        self.always_top_check = QCheckBox("Her zaman üstte / Always on top")
        self.always_top_check.setChecked(True)
        appearance_layout.addWidget(self.always_top_check)
        
        self.mini_mode_check = QCheckBox("Mini mod / Mini mode (genişleme yok)")
        appearance_layout.addWidget(self.mini_mode_check)
        
        # Button size slider
        size_layout = QHBoxLayout()
        size_label = QLabel("Buton boyutu / Button size:")
        self.size_value_label = QLabel("32")
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(24, 48)
        self.size_slider.setValue(32)
        self.size_slider.valueChanged.connect(self._on_size_change)
        
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_slider)
        size_layout.addWidget(self.size_value_label)
        appearance_layout.addLayout(size_layout)
        
        layout.addWidget(appearance_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("Kaydet / Save")
        save_btn.clicked.connect(self._save_settings)
        btn_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("Konumu Sıfırla / Reset Position")
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER};
            }}
        """)
        reset_btn.clicked.connect(self._reset_position)
        btn_layout.addWidget(reset_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
    def _load_settings(self):
        if self.parent_window:
            settings = self.parent_window.settings
            self.startup_check.setChecked(settings.value("startup_enabled", False, type=bool))
            self.always_top_check.setChecked(settings.value("always_on_top", True, type=bool))
            self.mini_mode_check.setChecked(settings.value("mini_mode", False, type=bool))
            btn_size = settings.value("button_size", 32, type=int)
            self.size_slider.setValue(btn_size)
            self.size_value_label.setText(str(btn_size))
            
    def _on_size_change(self, value):
        self.size_value_label.setText(str(value))
            
    def _save_settings(self):
        if self.parent_window:
            settings = self.parent_window.settings
            
            # Save startup setting
            startup_enabled = self.startup_check.isChecked()
            settings.setValue("startup_enabled", startup_enabled)
            self._set_startup(startup_enabled)
            
            # Save always on top setting
            always_top = self.always_top_check.isChecked()
            settings.setValue("always_on_top", always_top)
            self._apply_always_on_top(always_top)
            
            # Save mini mode
            mini_mode = self.mini_mode_check.isChecked()
            settings.setValue("mini_mode", mini_mode)
            self.parent_window.mini_mode = mini_mode
            
            # Save button size
            btn_size = self.size_slider.value()
            settings.setValue("button_size", btn_size)
            self.parent_window._apply_button_size(btn_size)
            
        self.accept()
        
    def _set_startup(self, enabled):
        """Add/remove from Windows startup"""
        if sys.platform == 'win32':
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "DynamicIslandSpotify"
            
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                if enabled:
                    # Get the path to the exe or python script
                    if getattr(sys, 'frozen', False):
                        exe_path = sys.executable
                    else:
                        exe_path = f'pythonw "{os.path.abspath(__file__)}"'
                    winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
                else:
                    try:
                        winreg.DeleteValue(key, app_name)
                    except FileNotFoundError:
                        pass
                winreg.CloseKey(key)
            except Exception as e:
                print(f"Startup registry error: {e}")
                
    def _apply_always_on_top(self, enabled):
        if self.parent_window:
            flags = self.parent_window.windowFlags()
            if enabled:
                flags |= Qt.WindowStaysOnTopHint
            else:
                flags &= ~Qt.WindowStaysOnTopHint
            self.parent_window.setWindowFlags(flags)
            self.parent_window.show()
            
    def _reset_position(self):
        if self.parent_window:
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - Config.COLLAPSED_W) // 2
            self.parent_window.move(x, 10)
            self.parent_window.settings.remove("pos_x")
            self.parent_window.settings.remove("pos_y")
