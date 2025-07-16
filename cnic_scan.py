import os
import time
import subprocess
import threading
import json
import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Tk, Label
from ttkbootstrap import Window
from PIL import Image, ImageTk


# Configuration
DEMO_PATH = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\bin\Release\Demo.exe'
WH_PATH = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\wh.jpg'
OCR_SCRIPT = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\ocr_doctr.py'
FLASK_URL = 'http://localhost:5000/check_cnic'
POLL_INTERVAL = 1000  # ms

# GUI Setup
root = Window(title="CNIC Scanner", themename="superhero", size=(750, 500), resizable=(False, False))

# --- Background Image ---
bg_img = Image.open("images/blur_cnic.png").resize((750, 500))
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = Label(root, image=bg_photo, borderwidth=0)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --- Top Bar ---
logo_img = Image.open("images/logo_pso.png").resize((50, 50))
logo_photo = ImageTk.PhotoImage(logo_img)
logo_label = Label(root, image=logo_photo, bg=None, borderwidth=0)
logo_label.image = logo_photo
logo_label.place(x=20, y=10)

title_label = Label(root, text="CNIC Scanner & Verifier", font=("Segoe UI", 24, "bold"), fg="white", bg=None)
title_label.place(x=90, y=20)

# --- Info Block (keep ttk) ---
info_frame = ttk.Frame(root, style="TFrame", padding=20)
info_frame.place(relx=0.5, rely=0.45, anchor="center")

cnic_text = ttk.Label(info_frame, text="CNIC:", font=("Segoe UI", 14))
cnic_text.pack(anchor="w")

name_text = ttk.Label(info_frame, text="Name:", font=("Segoe UI", 14))
name_text.pack(anchor="w")

# --- Status Label ---
status_label = ttk.Label(root, text="Status: Ready", font=("Segoe UI", 16), bootstyle=INFO)
status_label.place(relx=0.5, rely=0.70, anchor="center")

# --- Result Label ---
result_label = ttk.Label(root, text="", font=("Consolas", 12), foreground="white", background="")
result_label.place(relx=0.5, rely=0.80, anchor="center")

# --- Progress Bar ---
progress = ttk.Progressbar(root, mode='indeterminate', bootstyle=INFO)
progress.place(relx=0.5, rely=0.76, anchor="center")
progress.pack_forget()

# --- Footer + StingRey Logo ---
footer = Label(root, text="Powered by StingRey Tech", font=("Segoe UI", 10), fg="white", bg=None)
footer.place(x=20, y=470)

sting_img = Image.open("images/sray-removebg.png").resize((50, 50))
sting_photo = ImageTk.PhotoImage(sting_img)
sting_label = Label(root, image=sting_photo, bg=None, borderwidth=0)
sting_label.image = sting_photo
sting_label.place(x=680, y=445)



# --- UI State Functions ---
def set_scanning_ui():
    status_label.config(text="Scanning...", bootstyle=PRIMARY)
    progress.place(relx=0.5, rely=0.76, anchor="center")
    progress.start()
    result_label.config(text="", foreground="white")
    root.update()

def set_ocr_ui():
    status_label.config(text="Running OCR...", bootstyle=WARNING)
    root.update()

def set_ready_ui():
    status_label.config(text="Ready for next card", bootstyle=SUCCESS)
    progress.stop()
    progress.place_forget()
    root.update()

def set_remove_card_ui():
    status_label.config(text="Please remove card...", bootstyle=INFO)
    root.update()

def set_access_ui(granted):
    if granted:
        status_label.config(text="✅ ACCESS GRANTED", bootstyle=SUCCESS)
        result_label.config(foreground="green")
    else:
        status_label.config(text="❌ ACCESS DENIED", bootstyle=DANGER)
        result_label.config(foreground="red")
    root.update()

# --- Main OCR Function ---
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
        name = fields.get("Name", "Unknown").strip()
        # dob = fields.get("DoB", "N/A").strip()

        if not cnic:
            raise ValueError("CNIC not found in scan")

        # Update the info block
        cnic_text.config(text=f"CNIC: {cnic}")
        name_text.config(text=f"Name: {name}")
        # dob_text.config(text=f"DoB: {dob}")

        # Send CNIC to backend
        response = requests.post(FLASK_URL, json={'cnic': cnic}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'approved':
                set_access_ui(True)
                result_label.config(text=f"CNIC: {cnic}\nSTATUS: APPROVED")
            else:
                set_access_ui(False)
                result_label.config(text=f"CNIC: {cnic}\nSTATUS: NOT FOUND")
        else:
            set_access_ui(False)
            result_label.config(text=f"CNIC: {cnic}\nSERVER ERROR", foreground="orange")

    except Exception as e:
        result_label.config(text=f"ERROR: {str(e)}", foreground="red")
        set_access_ui(False)
    root.update()

# --- Polling Loop ---
def get_card_status():
    subprocess.run([DEMO_PATH, "--write-card-status"], creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        with open("card_status.txt", "r") as f:
            return f.read().strip() == "2"
    except Exception:
        return False

def polling_loop():
    while True:
        if os.path.exists(WH_PATH):
            set_scanning_ui()
            set_ocr_ui()
            run_ocr()
            set_remove_card_ui()

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

# --- Init Cleanup ---
if os.path.exists(WH_PATH):
    try:
        os.remove(WH_PATH)
    except Exception:
        pass

# --- Start Polling ---
threading.Thread(target=polling_loop, daemon=True).start()
root.mainloop()
