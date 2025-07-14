import os
import time
import subprocess
import threading
import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests

# Configuration - using raw strings for Windows paths
DEMO_PATH = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\bin\Release\Demo.exe'
WH_PATH = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\wh.jpg'
OCR_SCRIPT = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\ocr_doctr.py'
FLASK_URL = 'http://localhost:5000/check_cnic'
POLL_INTERVAL = 1000  # ms

def get_card_status():
    subprocess.run([DEMO_PATH, "--write-card-status"], creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        with open("card_status.txt", "r") as f:
            return f.read().strip() == "2"
    except Exception:
        return False

def set_scanning_ui():
    status_label.config(text="Scanning...", bootstyle=PRIMARY)
    progress.pack(pady=(0, 10))
    progress.start()
    cnic_label.config(text="")
    result_label.config(text="")
    root.update()

def set_ocr_ui():
    status_label.config(text="Running OCR...", bootstyle=WARNING)
    root.update()

def set_ready_ui():
    status_label.config(text="Ready for next card", bootstyle=SUCCESS)
    progress.stop()
    progress.pack_forget()
    root.update()

def set_remove_card_ui():
    status_label.config(text="Please remove card...", bootstyle=INFO)
    root.update()

def set_access_ui(granted):
    if granted:
        status_label.config(text="ACCESS GRANTED", bootstyle=SUCCESS)
        result_label.config(foreground="green")
    else:
        status_label.config(text="ACCESS DENIED", bootstyle=DANGER)
        result_label.config(foreground="red")
    root.update()

def run_ocr():
    try:
        result = subprocess.run(
            ["python", OCR_SCRIPT, WH_PATH],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(OCR_SCRIPT)
        )
        fields = json.loads(result.stdout.strip())
        cnic = fields.get("CNIC Number", "").strip()
        if not cnic:
            raise ValueError("CNIC not found in scan")
        
        # Only send CNIC to backend
        response = requests.post(
            FLASK_URL,
            json={'cnic': cnic},  # Only sending CNIC, ignoring name
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'approved':
                set_access_ui(True)
                result_label.config(text=f"CNIC: {cnic}\nSTATUS: APPROVED", 
                                  foreground="green")
            else:
                set_access_ui(False)
                result_label.config(text=f"CNIC: {cnic}\nSTATUS: NOT FOUND", 
                                  foreground="red")
        else:
            set_access_ui(False)
            result_label.config(text=f"CNIC: {cnic}\nSERVER ERROR", 
                              foreground="orange")
            
    except Exception as e:
        result_label.config(text=f"ERROR: {str(e)}", foreground="red")
        set_access_ui(False)
    
    root.update()

def polling_loop():
    while True:
        if os.path.exists(WH_PATH):
            set_scanning_ui()
            set_ocr_ui()
            run_ocr()
            set_remove_card_ui()
            
            # Wait until card is removed
            while get_card_status():
                time.sleep(0.5)
            
            try:
                os.remove(WH_PATH)
            except Exception:
                pass
                
            set_ready_ui()
        else:
            if get_card_status():
                set_scanning_ui()
            subprocess.run([DEMO_PATH, "--silent"], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(POLL_INTERVAL / 1000)

# GUI Setup
root = ttk.Window(themename="superhero")
root.title("CNIC Scanner")
root.geometry("750x500")
root.resizable(False, False)

title_label = ttk.Label(root, text="CNIC Scanner", font=("Segoe UI", 26, "bold"), bootstyle=PRIMARY)
title_label.pack(pady=(20, 10))

status_label = ttk.Label(root, text="Ready", font=("Segoe UI", 16), bootstyle=INFO)
status_label.pack(pady=(0, 15))

cnic_label = ttk.Label(root, text="", font=("Segoe UI", 22, "bold"))
cnic_label.pack()

progress = ttk.Progressbar(root, mode='indeterminate', bootstyle=INFO)
progress.pack_forget()

result_label = ttk.Label(root, text="", font=("Consolas", 12), wraplength=700, justify="left")
result_label.pack(fill="both", expand=True, padx=20, pady=10)

if os.path.exists(WH_PATH):
    try:
        os.remove(WH_PATH)
    except Exception:
        pass

threading.Thread(target=polling_loop, daemon=True).start()
root.mainloop()