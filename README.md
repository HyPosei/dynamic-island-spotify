# 🎵 Dynamic Island Spotify Controller

A polished, macOS-inspired Dynamic Island widget for Windows that provides real-time Spotify playback control with smooth animations and dynamic theming based on album artwork.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Spotify OAuth Integration** | Secure authentication with automatic token refresh |
| **Real-time Now Playing** | Instant track detection with artist and album info |
| **Dynamic Color Theming** | UI colors automatically adapt to album artwork |
| **Smooth Animations** | GPU-accelerated Qt6 animations for fluid UX |
| **Full Playback Control** | Play, pause, skip, shuffle, repeat, and volume |
| **Seek Bar** | Visual progress with drag-to-seek functionality |
| **Like/Unlike Tracks** | Quick access to save tracks to your library |
| **Rate Limit Handling** | Graceful handling of Spotify API limits |
| **Windows Native** | Designed specifically for Windows 10/11 |
| **Minimal Footprint** | Collapses to a compact pill when not in use |

---

## 🎬 Demo

> **Video demonstration coming soon**

### Screenshots

<p align="center">
  <img src="docs/screenshots/collapsed.png" alt="Collapsed State" width="300"/>
  <img src="docs/screenshots/expanded.png" alt="Expanded State" width="400"/>
</p>

---

## 🚀 Quick Start

### Prerequisites

- **Windows 10/11**
- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Spotify Premium** (required for playback control)

### Installation

#### Option 1: Automated Setup (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/dynamic-island-spotify.git
cd dynamic-island-spotify

# 2. Run setup script
setup.bat
```

The setup script will:
- Create a virtual environment
- Install all dependencies
- Guide you through Spotify API configuration

#### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
notepad .env  # Add your Spotify credentials

# Run the application
python dynamic_island.py
```

### Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **Create App**
3. Configure your application:
   - **App name:** Dynamic Island
   - **Redirect URI:** `http://localhost:8888/callback`
   - **APIs:** Select **Web API**
4. Copy your **Client ID** and **Client Secret**
5. Add them to your `.env` file

---

## 🏗️ Architecture

```
dynamic-island-spotify/
├── dynamic_island.py      # Main application entry point
├── spotify_watcher.py     # Background Spotify monitor
├── core/
│   ├── config.py          # Configuration and constants
│   ├── spotify_worker.py  # Spotify API integration
│   ├── widgets.py         # Custom Qt widgets
│   └── settings.py        # Settings dialog
├── docs/
│   └── screenshots/       # Demo images
├── setup.bat              # Automated setup script
├── run.bat                # Application launcher
└── requirements.txt       # Python dependencies
```

### Key Components

- **SpotifyWorker**: Background thread handling API polling with adaptive intervals
- **DynamicIsland**: Main Qt window with animation system
- **StyledButton**: Custom buttons with QtAwesome icons
- **ColorThief**: Extracts dominant colors from album artwork

---

## 🎮 Usage

| Action | Method |
|--------|--------|
| Expand widget | Hover mouse over island |
| Play/Pause | Click ▶️ / ⏸️ |
| Next/Previous | Click ⏭️ / ⏮️ |
| Toggle shuffle | Click 🔀 |
| Toggle repeat | Click 🔁 |
| Like track | Click ❤️ |
| Adjust volume | Use slider or scroll wheel |
| Seek | Drag progress bar |
| Settings | Right-click system tray |
| Exit | Right-click tray → Exit |

---

## 🛠️ Configuration

Edit `core/config.py` to customize:

```python
class Config:
    COLLAPSED_W, COLLAPSED_H = 200, 52    # Collapsed size
    EXPANDED_W, EXPANDED_H = 440, 150     # Expanded size
    ANIMATION_MS = 350                     # Animation duration
    POLL_FAST = 1.0                        # Polling interval (playing)
    POLL_SLOW = 3.0                        # Polling interval (paused)
```

---

## 🔐 Security

- **Never commit `.env`** — it contains your API secrets
- **`.spotify_cache`** stores OAuth tokens — keep it private
- See [SECURITY.md](SECURITY.md) for credential rotation instructions

---

## 📋 Requirements

```
PySide6>=6.5.0
spotipy>=2.23.0
python-dotenv>=1.0.0
Pillow>=10.0.0
requests>=2.31.0
colorthief>=0.2.1
psutil>=5.9.0
qtawesome>=1.2.0
```

---

## 🤖 AI Disclosure

AI-assisted development was used for prototyping and productivity during the development of this project. All architectural decisions, Spotify API integration, application logic, code refactoring, and testing were owned and reviewed by me.

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## ⚠️ Disclaimer

This project is **not affiliated with, endorsed by, or sponsored by Spotify AB or Apple Inc.**

- "Spotify" is a registered trademark of Spotify AB
- "Dynamic Island" is a trademark of Apple Inc.
- This is an independent, open-source project for educational and personal use

---

<div align="center">

**Made with ❤️ for music lovers**

If you find this useful, consider giving it a ⭐

</div>
