import os
import time
import subprocess
import threading
import json
import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Tk, Label
import tkinter as tk
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

# --- Canvas Setup ---
canvas = tk.Canvas(root, width=750, height=500, highlightthickness=0)
canvas.place(x=0, y=0)

# --- Background Image ---
bg_img = Image.open("images/blur_cnic.png").resize((750, 500))
bg_photo = ImageTk.PhotoImage(bg_img)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# --- Logos ---
logo_img = Image.open("images/logo_pso.png").resize((50, 50))
logo_photo = ImageTk.PhotoImage(logo_img)
canvas.create_image(20, 10, anchor="nw", image=logo_photo)

sting_img = Image.open("images/sray-removebg.png").resize((50, 50))
sting_photo = ImageTk.PhotoImage(sting_img)
canvas.create_image(680, 445, anchor="nw", image=sting_photo)

# --- Text on Canvas (no shading!) ---
canvas.create_text(90, 30, anchor="nw",
                   text="CNIC Scanner & Verifier",
                   font=("Segoe UI", 24, "bold"),
                   fill="white")

status_text = canvas.create_text(375, 350, anchor="center",
                                 text="Status: Ready",
                                 font=("Segoe UI", 16),
                                 fill="white")

result_text = canvas.create_text(375, 400, anchor="center",
                                 text="",
                                 font=("Consolas", 12),
                                 fill="white")

canvas.create_text(20, 470, anchor="nw",
                   text="Powered by StingRey Tech",
                   font=("Segoe UI", 10),
                   fill="white")

# --- Info Frame (keep form clean here) ---
info_frame = ttk.Frame(root, padding=20)
info_frame.place(relx=0.5, rely=0.45, anchor="center")

ttk.Label(info_frame, text="CNIC:", font=("Segoe UI", 14)).pack(anchor="w")
ttk.Label(info_frame, text="Name:", font=("Segoe UI", 14)).pack(anchor="w")

# --- Progress Bar ---
progress = ttk.Progressbar(root, mode='indeterminate', bootstyle="striped", length=200)
progress.place(relx=0.5, rely=0.76, anchor="center")
progress.pack_forget()

# --- Store references for updates ---
def update_status(msg):
    canvas.itemconfig(status_text, text=msg)

def update_result(msg):
    canvas.itemconfig(result_text, text=msg)

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
