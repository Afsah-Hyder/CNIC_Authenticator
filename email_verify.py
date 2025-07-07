import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid
import qrcode
import base64
from io import BytesIO
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("cnic_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cnic_records (
            cnic_number TEXT PRIMARY KEY,
            name TEXT,
            father_name TEXT,
            address TEXT,
            authorization_status TEXT,
            added_by TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Add or update CNIC in database with authorization status
def update_db(cnic_number, name, father_name, address, authorization_status, added_by):
    conn = sqlite3.connect("cnic_database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO cnic_records 
        (cnic_number, name, father_name, address, authorization_status, added_by) 
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (cnic_number, name, father_name, address, authorization_status, added_by)
    )
    conn.commit()
    conn.close()

# Generate secure token for email link
def generate_token(cnic_number):
    return str(uuid.uuid4())

# Generate QR code for email link
def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Send email with CNIC details and authorization options
def send_email(cnic_data, recipient_email):
    sender_email = "your_email@example.com"  # Replace with your email
    password = "your_app_password"  # Use app-specific password for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "CNIC Authorization Request"

    # Email body
    token = generate_token(cnic_data["cnic_number"])
    auth_url = f"http://yourserver.com/authorize?cnic={cnic_data['cnic_number']}&token={token}&status=Authorized"
    deny_url = f"http://yourserver.com/authorize?cnic={cnic_data['cnic_number']}&token={token}&status=Not%20Authorized"
    qr_auth = generate_qr_code(auth_url)
    qr_deny = generate_qr_code(deny_url)

    body = f"""
    <h3>CNIC Authorization Request</h3>
    <p>Please review the following CNIC details and confirm authorization:</p>
    <ul>
        <li><b>CNIC Number</b>: {cnic_data['cnic_number']}</li>
        <li><b>Name</b>: {cnic_data['name']}</li>
        <li><b>Father's Name</b>: {cnic_data['father_name']}</li>
        <li><b>Address</b>: {cnic_data['address']}</li>
    </ul>
    <p><a href="{auth_url}">Click here to Authorize</a></p>
    <p><img src="data:image/png;base64,{qr_auth}" alt="Authorize QR Code"/></p>
    <p><a href="{deny_url}">Click here to Deny Authorization</a></p>
    <p><img src="data:image/png;base64,{qr_deny}" alt="Deny QR Code"/></p>
    """

    msg.attach(MIMEText(body, "html"))

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

# Extract CNIC details using OCR (doctr)
def extract_cnic_details(image_path):
    predictor = ocr_predictor(pretrained=True)
    doc = DocumentFile.from_images(image_path)
    result = predictor(doc)
    text = result.render()
    # Simulated parsing (replace with actual text parsing logic)
    cnic_data = {
        "cnic_number": "1234567890123",  # Extract from text
        "name": "Ali Khan",              # Extract from text
        "father_name": "Ahmed Khan",     # Extract from text
        "address": "123 Street, Karachi"  # Extract from text
    }
    return cnic_data

# Flask endpoint to handle CNIC scan
@app.route("/scan_cnic", methods=["POST"])
def scan_cnic():
    file = request.files.get("image")
    recipient_email = request.form.get("email")
    if not file or not recipient_email:
        return jsonify({"error": "Image and email required"}), 400

    # Save uploaded image
    image_path = "temp_cnic.jpg"
    file.save(image_path)

    # Extract CNIC details
    cnic_data = extract_cnic_details(image_path)

    # Send email with authorization options
    send_email(cnic_data, recipient_email)
    return jsonify({"message": "Authorization request email sent", "cnic_data": cnic_data})

# Flask endpoint to handle authorization response
@app.route("/authorize", methods=["GET"])
def authorize():
    cnic_number = request.args.get("cnic")
    token = request.args.get("token")
    status = request.args.get("status")
    
    # Validate token (implement token storage/verification in production)
    if not cnic_number or not token or not status:
        return jsonify({"error": "Invalid request"}), 400

    # Simulated CNIC details (in production, retrieve from temp storage or session)
    cnic_data = {
        "cnic_number": cnic_number,
        "name": "Ali Khan",
        "father_name": "Ahmed Khan",
        "address": "123 Street, Karachi"
    }

    # Update database with authorization status
    update_db(
        cnic_number,
        cnic_data["name"],
        cnic_data["father_name"],
        cnic_data["address"],
        status,
        "admin@example.com"  # Replace with authenticated user
    )
    return jsonify({"message": f"CNIC {cnic_number} marked as {status} in database"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)