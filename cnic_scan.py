# import os
# import time
# import subprocess
# import threading
# import json
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *

# DEMO_PATH = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\bin\Release\Demo.exe'
# WH_PATH = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\wh.jpg'
# OCR_SCRIPT = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\ocr_doctr.py'
# OCR_IMG_ARG = r'wh.jpg'

# POLL_INTERVAL = 1000  # ms

# def get_card_status():
#     subprocess.run([DEMO_PATH, "--write-card-status"], creationflags=subprocess.CREATE_NO_WINDOW)
#     try:
#         with open("card_status.txt", "r") as f:
#             status = f.read().strip()
#             return status == "2"
#     except Exception:
#         return False

# def set_scanning_ui():
#     status_label.config(text="Scanning...", bootstyle=PRIMARY)
#     status_label.config(font=("Segoe UI", 16, "bold"))
#     progress.pack(pady=(0, 10))
#     progress.start()
#     cnic_label.config(text="", background="#222831")  # <-- Clear CNIC number here
#     result_label.config(text="", background="#222831", foreground="#eeeeee")
#     root.update_idletasks()

# def set_ocr_ui():
#     status_label.config(text="Running OCR...", bootstyle=WARNING)
#     status_label.config(font=("Segoe UI", 16, "bold"))
#     root.update_idletasks()

# def set_ready_ui():
#     status_label.config(text="Ready for next card.", bootstyle=SUCCESS)
#     status_label.config(font=("Segoe UI", 16, "bold"))
#     progress.stop()
#     progress.pack_forget()
#     result_label.config(background="#222831", foreground="#eeeeee")
#     root.update_idletasks()

# def set_remove_card_ui():
#     status_label.config(text="Please remove card...", bootstyle=INFO)
#     status_label.config(font=("Segoe UI", 16, "bold"))
#     root.update_idletasks()

# def polling_loop():
#     while True:
#         if os.path.exists(WH_PATH):
#             set_scanning_ui()
#             set_ocr_ui()
#             run_ocr()
#             set_remove_card_ui()
#             # Wait until card is removed
#             while get_card_status():
#                 time.sleep(0.5)
#             try:
#                 os.remove(WH_PATH)
#             except Exception:
#                 pass
#             set_ready_ui()
#         else:
#             if get_card_status():  # Card is present, about to scan
#                 set_scanning_ui()
#             subprocess.run([DEMO_PATH, "--silent"], creationflags=subprocess.CREATE_NO_WINDOW)
#         time.sleep(POLL_INTERVAL / 1000.0)

# def run_ocr():
#     ocr_cmd = ["python", OCR_SCRIPT, OCR_IMG_ARG]
#     result = subprocess.run(ocr_cmd, cwd=os.path.dirname(OCR_SCRIPT), capture_output=True, text=True)
#     ocr_text = result.stdout.strip()
#     error_text = result.stderr.strip()

#     try:
#         fields = json.loads(ocr_text)
#         # Display CNIC Number first, in large/bold font
#         cnic = fields.get("CNIC Number", "Not found")
#         cnic_label.config(text=cnic, font=("Segoe UI", 22, "bold"), foreground="#1e90ff", background="#222831")
#         display = ""
#         for key in ["Name", "Father Name", "Date of Birth", "Gender", "Country of Stay"]:
#             value = fields.get(key, "")
#             if value:
#                 display += f"{key}: {value}\n"
#         result_label.config(text=display, font=("Consolas", 16, "bold"), background="#222831", foreground="#eeeeee", anchor="nw", justify="left")
#     except Exception:
#         cnic_label.config(text="", background="#222831")
#         result_label.config(text=ocr_text if ocr_text else (error_text or "No OCR result."),
#                             font=("Consolas", 16, "bold"), background="#222831", foreground="#eeeeee", anchor="nw", justify="left")
#     root.update_idletasks()

# root = ttk.Window(themename="superhero")
# root.title("CNIC OCR Scan")
# root.geometry("750x500")
# root.resizable(False, False)
# root.configure(background="#222831")

# title_label = ttk.Label(root, text="CNIC OCR Scan", font=("Segoe UI", 26, "bold"), bootstyle=PRIMARY, background="#222831")
# title_label.pack(pady=(28, 16))

# status_label = ttk.Label(root, text="Ready", font=("Segoe UI", 16, "bold"), bootstyle=INFO, background="#222831")
# status_label.pack(pady=(0, 18))

# cnic_label = ttk.Label(root, text="", font=("Segoe UI", 22, "bold"), foreground="#1e90ff", background="#222831", anchor="center")
# cnic_label.pack(pady=(0, 0))

# progress = ttk.Progressbar(root, mode='indeterminate', bootstyle=INFO)
# progress.pack_forget()  # Hide initially

# result_label = ttk.Label(root, text="", font=("Segoe UI", 16), background="#222831", foreground="#eeeeee", anchor="nw", justify="left")
# result_label.pack(fill="both", expand=True, padx=30, pady=16)

# if os.path.exists(WH_PATH):
#     try:
#         os.remove(WH_PATH)
#     except Exception:
#         pass

# # Start the polling loop in a background thread
# threading.Thread(target=polling_loop, daemon=True).start()

# root.mainloop()

import os
import time
import subprocess
import threading
import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests  # Added for HTTP requests

DEMO_PATH = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\bin\Release\Demo.exe'
WH_PATH = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\wh.jpg'
OCR_SCRIPT = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\ocr_doctr.py'
OCR_IMG_ARG = r'wh.jpg'
FLASK_URL = 'http://localhost:5000/store_cnic'  # Added for Flask server

POLL_INTERVAL = 1000  # ms

def get_card_status():
    subprocess.run([DEMO_PATH, "--write-card-status"], creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        with open("card_status.txt", "r") as f:
            status = f.read().strip()
            return status == "2"
    except Exception:
        return False

def set_scanning_ui():
    status_label.config(text="Scanning...", bootstyle=PRIMARY)
    status_label.config(font=("Segoe UI", 16, "bold"))
    progress.pack(pady=(0, 10))
    progress.start()
    cnic_label.config(text="", background="#222831")
    result_label.config(text="", background="#222831", foreground="#eeeeee")
    root.update_idletasks()

def set_ocr_ui():
    status_label.config(text="Running OCR...", bootstyle=WARNING)
    status_label.config(font=("Segoe UI", 16, "bold"))
    root.update_idletasks()

def set_ready_ui():
    status_label.config(text="Ready for next card.", bootstyle=SUCCESS)
    status_label.config(font=("Segoe UI", 16, "bold"))
    progress.stop()
    progress.pack_forget()
    result_label.config(background="#222831", foreground="#eeeeee")
    root.update_idletasks()

def set_remove_card_ui():
    status_label.config(text="Please remove card...", bootstyle=INFO)
    status_label.config(font=("Segoe UI", 16, "bold"))
    root.update_idletasks()

def run_ocr():
    ocr_cmd = ["python", OCR_SCRIPT, OCR_IMG_ARG]
    result = subprocess.run(ocr_cmd, cwd=os.path.dirname(OCR_SCRIPT), capture_output=True, text=True)
    ocr_text = result.stdout.strip()
    error_text = result.stderr.strip()

    try:
        fields = json.loads(ocr_text)
        # Display CNIC Number first, in large/bold font
        cnic = fields.get("CNIC Number", "Not found")
        cnic_label.config(text=cnic, font=("Segoe UI", 22, "bold"), foreground="#1e90ff", background="#222831")
        display = ""
        for key in ["Name", "Father Name", "Date of Birth", "Gender", "Country of Stay"]:
            value = fields.get(key, "")
            if value:
                display += f"{key}: {value}\n"
        result_label.config(text=display, font=("Consolas", 16, "bold"), background="#222831", foreground="#eeeeee", anchor="nw", justify="left")
        
        # Send OCR results to Flask server
        try:
            response = requests.post(FLASK_URL, json=fields)
            if response.status_code == 200:
                result_label.config(text=display + "\nData sent to server successfully.", foreground="#00ff00")
            else:
                result_label.config(text=display + f"\nFailed to send data to server: {response.status_code}", foreground="#ff0000")
        except requests.RequestException as e:
            result_label.config(text=display + f"\nServer connection error: {str(e)}", foreground="#ff0000")
            
    except Exception:
        cnic_label.config(text="", background="#222831")
        result_label.config(text=ocr_text if ocr_text else (error_text or "No OCR result."),
                           font=("Consolas", 16, "bold"), background="#222831", foreground="#eeeeee", anchor="nw", justify="left")
    root.update_idletasks()

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
            if get_card_status():  # Card is present, about to scan
                set_scanning_ui()
            subprocess.run([DEMO_PATH, "--silent"], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(POLL_INTERVAL / 1000.0)

root = ttk.Window(themename="superhero")
root.title("CNIC OCR Scan")
root.geometry("750x500")
root.resizable(False, False)
root.configure(background="#222831")

title_label = ttk.Label(root, text="CNIC OCR Scan", font=("Segoe UI", 26, "bold"), bootstyle=PRIMARY, background="#222831")
title_label.pack(pady=(28, 16))

status_label = ttk.Label(root, text="Ready", font=("Segoe UI", 16, "bold"), bootstyle=INFO, background="#222831")
status_label.pack(pady=(0, 18))

cnic_label = ttk.Label(root, text="", font=("Segoe UI", 22, "bold"), foreground="#1e90ff", background="#222831", anchor="center")
cnic_label.pack(pady=(0, 0))

progress = ttk.Progressbar(root, mode='indeterminate', bootstyle=INFO)
progress.pack_forget()  # Hide initially

result_label = ttk.Label(root, text="", font=("Segoe UI", 16), background="#222831", foreground="#eeeeee", anchor="nw", justify="left")
result_label.pack(fill="both", expand=True, padx=30, pady=16)

if os.path.exists(WH_PATH):
    try:
        os.remove(WH_PATH)
    except Exception:
        pass

# Start the polling loop in a background thread
threading.Thread(target=polling_loop, daemon=True).start()

root.mainloop()