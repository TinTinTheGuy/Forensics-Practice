import psutil
import ctypes
import win32gui
import win32process
import os

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Function to check if a process has loaded user32.dll (often required for keylogging)
def check_user32_dll(pid):
    try:
        process = psutil.Process(pid)
        for module in process.memory_maps():
            if "user32.dll" in module.path.lower():
                return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    return False

# Function to scan suspicious processes
def detect_suspicious_processes():
    print("[INFO] Scanning for potential keyloggers...")

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pid = proc.info['pid']
            proc_name = proc.info['name'].lower()

            # Get process window handle
            hwnd = win32gui.GetForegroundWindow()
            _, foreground_pid = win32process.GetWindowThreadProcessId(hwnd)

            # If process is running in the foreground and has user32.dll, it's suspicious
            if pid == foreground_pid and check_user32_dll(pid):
                print(f"[WARNING] Suspicious process detected: {proc_name} (PID: {pid})")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

if __name__ == "__main__":
    detect_suspicious_processes()
