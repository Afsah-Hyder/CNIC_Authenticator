import os
import time
import subprocess
import threading
import json
import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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
root = Window(title="CNIC Scanner", themename="superhero", size=(1024, 600), resizable=(False, False))

# --- Canvas Setup ---
canvas = tk.Canvas(root, width=1024, height=600, highlightthickness=0)
canvas.place(x=0, y=0)

# --- Load new full background image (with logos, title, footer baked in) ---
bg_img = Image.open("images/ttk_bg.png").resize((1024, 600))
bg_photo = ImageTk.PhotoImage(bg_img)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# --- Info Labels for CNIC and Name -- placed roughly center over the baked-in textbox ---
info_frame = ttk.Frame(root)
info_frame.place(relx=0.55, rely=0.475, anchor="center")

cnic_text = ttk.Label(info_frame, text="CNIC: xxxxx-xxxxxxx-x", font=("Segoe UI", 14), style="My.TLabel")
cnic_text.pack(anchor="center", pady=(0, 5))

name_text = ttk.Label(info_frame, text="Name: John Doe", font=("Segoe UI", 14), style="My.TLabel")
name_text.pack(anchor="center")

info_frame.configure(style="My.TFrame")
style = ttk.Style()
style.configure("My.TFrame", background="#6e8f6f")
cnic_text.configure(background="#6e8f6f")
name_text.configure(background="#6e8f6f")

# --- Progress Bar ---
progress = ttk.Progressbar(root, mode='indeterminate', bootstyle="striped", length=400)
progress.place(relx=0.5, rely=0.90, anchor="center")
progress.pack_forget()

# --- Status and Result texts as canvas text items ---
status_text_id = canvas.create_text(450, 470, text="Status: Ready", font=("Segoe UI", 16), fill="white", anchor="nw")
error_text_id = canvas.create_text(440, 330, text="", font=("Helvetica", 15, "bold"), fill="white", anchor="nw")

# --- Canvas Update Functions ---
def update_status(msg, color="white"):
    canvas.itemconfig(status_text_id, text=msg, fill=color)

def update_result(msg, color="white"):
    canvas.itemconfig(error_text_id, text=msg, fill=color)

# --- UI State Handlers ---
def set_scanning_ui():
    update_status("Scanning...", color="white")
    progress.place(relx=0.5, rely=0.90, anchor="center")
    progress.start()
    update_result("")
    root.update()

def set_ocr_ui():
    update_status("Running OCR...", color="white")
    root.update()

def set_ready_ui():
    update_status("Ready for next card", color="white")
    progress.stop()
    progress.place_forget()
    update_result("")
    root.update()

def set_remove_card_ui():
    update_status("Please remove card...", color="white")
    root.update()

def set_access_ui(granted):
    if granted:
        update_result("\u2705 ACCESS GRANTED", color="#4CAF50")
    else:
        update_result("\u274C ACCESS DENIED", color="#F44336")
    root.update()

# --- Main OCR Function ---
def run_ocr():
    try:
        result = subprocess.run([
            "python", OCR_SCRIPT, WH_PATH
        ], capture_output=True, text=True, cwd=os.path.dirname(OCR_SCRIPT))

        fields = json.loads(result.stdout.strip())
        cnic = fields.get("CNIC Number", "").strip()
        name = fields.get("Name", "Unknown").strip()

        if not cnic:
            raise ValueError("CNIC not found in scan")

        cnic_text.config(text=f"CNIC: {cnic}")
        name_text.config(text=f"Name: {name}")

        response = requests.post(FLASK_URL, json={'cnic': cnic}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            set_access_ui(data.get('status') == 'approved')
        else:
            update_result("SERVER ERROR", color="#004aad")
    
    except Exception as e:
        update_result(f"ERROR: {str(e)}", color="red")
        set_access_ui(False)
    root.update()

# --- Card Reader Polling ---
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

# --- Cleanup and Startup ---
if os.path.exists(WH_PATH):
    try:
        os.remove(WH_PATH)
    except Exception:
        pass

threading.Thread(target=polling_loop, daemon=True).start()
root.mainloop()
