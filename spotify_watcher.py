"""
🔍 Spotify Watcher
━━━━━━━━━━━━━━━━━━
Monitors Spotify process and automatically launches Dynamic Island when Spotify opens.
Runs silently in the background with minimal resource usage.
"""

import subprocess
import sys
import os
import time
import psutil

# Configuration
CHECK_INTERVAL = 3  # Seconds between checks
SPOTIFY_PROCESS = "Spotify.exe"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DYNAMIC_ISLAND_SCRIPT = os.path.join(SCRIPT_DIR, "dynamic_island.py")


def is_process_running(process_name):
    """Check if a process is currently running"""
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def is_dynamic_island_running():
    """Check if Dynamic Island is already running"""
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] == current_pid:
                continue
            cmdline = proc.info.get('cmdline') or []
            cmdline_str = ' '.join(cmdline).lower()
            if 'dynamic_island.py' in cmdline_str and 'python' in proc.info.get('name', '').lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def launch_dynamic_island():
    """Launch Dynamic Island script"""
    if not os.path.exists(DYNAMIC_ISLAND_SCRIPT):
        print(f"[!] Dynamic Island script not found: {DYNAMIC_ISLAND_SCRIPT}")
        return False
    
    try:
        # Use pythonw for silent execution (no console window)
        python_exe = sys.executable
        pythonw_exe = python_exe.replace('python.exe', 'pythonw.exe')
        
        if os.path.exists(pythonw_exe):
            subprocess.Popen([pythonw_exe, DYNAMIC_ISLAND_SCRIPT], 
                           cwd=SCRIPT_DIR,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen([python_exe, DYNAMIC_ISLAND_SCRIPT], 
                           cwd=SCRIPT_DIR,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        
        print("[+] Dynamic Island launched!")
        return True
    except Exception as e:
        print(f"[!] Failed to launch Dynamic Island: {e}")
        return False


def main():
    print("[*] Spotify Watcher Started")
    print(f"    Checking every {CHECK_INTERVAL} seconds...")
    print("    Press Ctrl+C to stop\n")
    
    spotify_was_running = False
    
    try:
        while True:
            spotify_running = is_process_running(SPOTIFY_PROCESS)
            
            if spotify_running and not spotify_was_running:
                # Spotify just opened
                print("[+] Spotify detected!")
                time.sleep(2)  # Wait for Spotify to fully initialize
                
                if not is_dynamic_island_running():
                    launch_dynamic_island()
                else:
                    print("[i] Dynamic Island already running")
            
            elif not spotify_running and spotify_was_running:
                # Spotify closed
                print("[-] Spotify closed")
            
            spotify_was_running = spotify_running
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n[*] Watcher stopped")


if __name__ == "__main__":
    main()
