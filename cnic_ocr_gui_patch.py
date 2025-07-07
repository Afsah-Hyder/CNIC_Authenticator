import requests

def send_ocr_to_auth_server(ocr_data, recipient_email="admin@example.com"):
    try:
        response = requests.post(
            "http://localhost:5000/scan_cnic",
            json={"ocr_data": ocr_data, "email": recipient_email}
        )
        print(f"Sent OCR data to auth server: {response.status_code}")
    except Exception as e:
        print(f"Failed to send OCR data: {e}")

# Add this line in the run_ocr() function, after parsing JSON
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
        # Send OCR results to auth server
        send_ocr_to_auth_server(fields)  # Add this line
    except Exception:
        cnic_label.config(text="", background="#222831")
        result_label.config(text=ocr_text if ocr_text else (error_text or "No OCR result."),
                            font=("Consolas", 16, "bold"), background="#222831", foreground="#eeeeee", anchor="nw", justify="left")
    root.update_idletasks()