import sqlite3
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('cnic_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cnic_records
                 (id INTEGER PRIMARY KEY, cnic_number TEXT, name TEXT, fat2her_name TEXT,
                  dob TEXT, gender TEXT, country TEXT, status TEXT, token TEXT, token_created_at TEXT)''')
    conn.commit()
    conn.close()

# Send email with authorization links
def send_email(data, token):
    sender_email = "afsahyder.8@gmail.com"
    password = os.getenv("EMAIL_PASSWORD", "your_app_password")  # Use env variable
    receiver_email = "safahbilal13@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'CNIC Authorization Request'
    
    body = (f"CNIC Details:\n"
            f"CNIC Number: {data.get('CNIC Number', 'N/A')}\n"
            f"Name: {data.get('Name', 'N/A')}\n"
            f"Father Name: {data.get('Father Name', 'N/A')}\n"
            f"Date of Birth: {data.get('Date of Birth', 'N/A')}\n"
            f"Gender: {data.get('Gender', 'N/A')}\n"
            f"Country of Stay: {data.get('Country of Stay', 'N/A')}\n\n"
            f"Authorize: http://localhost:5000/authorize/{token}\n"
            f"Deny: http://localhost:5000/deny/{token}")
    message.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

# Store CNIC data and generate token
@app.route('/store_cnic', methods=['POST'])
def store_cnic():
    data = request.json
    token = str(uuid.uuid4())
    token_created_at = datetime.now().isoformat()
    
    conn = sqlite3.connect('cnic_database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO cnic_records (cnic_number, name, father_name, dob, gender, country, status, token, token_created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (data.get('CNIC Number'), data.get('Name'), data.get('Father Name'),
               data.get('Date of Birth'), data.get('Gender'), data.get('Country of Stay'),
               'pending', token, token_created_at))
    conn.commit()
    conn.close()
    
    send_email(data, token)
    return jsonify({'message': 'CNIC data stored and email sent', 'token': token})

# Check token expiration
def is_token_valid(token_created_at):
    created_time = datetime.fromisoformat(token_created_at)
    expiration_time = created_time + timedelta(hours=24)
    return datetime.now() < expiration_time

# Authorize endpoint
@app.route('/authorize/<token>', methods=['GET'])
def authorize(token):
    conn = sqlite3.connect('cnic_database.db')
    c = conn.cursor()
    c.execute('SELECT token_created_at FROM cnic_records WHERE token = ?', (token,))
    result = c.fetchone()
    if not result:
        conn.close()
        return jsonify({'error': 'Invalid token'})
    if not is_token_valid(result[0]):
        conn.close()
        return jsonify({'error': 'Token expired'})
    c.execute('UPDATE cnic_records SET status = ? WHERE token = ?', ('authorized', token))
    conn.commit()
    conn.close()
    return jsonify({'message': 'CNIC authorized'})

# Deny endpoint
@app.route('/deny/<token>', methods=['GET'])
def deny(token):
    conn = sqlite3.connect('cnic_database.db')
    c = conn.cursor()
    c.execute('SELECT token_created_at FROM cnic_records WHERE token = ?', (token,))
    result = c.fetchone()
    if not result:
        conn.close()
        return jsonify({'error': 'Invalid token'})
    if not is_token_valid(result[0]):
        conn.close()
        return jsonify({'error': 'Token expired'})
    c.execute('UPDATE cnic_records SET status = ? WHERE token = ?', ('denied', token))
    conn.commit()
    conn.close()
    return jsonify({'message': 'CNIC denied'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
