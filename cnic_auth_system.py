import sqlite3
import imaplib
import email
import re
from email.header import decode_header
from flask import Flask, request, jsonify
import os
import time
from threading import Thread
from datetime import datetime

app = Flask(__name__)

# Database setup
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cnic_database.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS guests
                 (id INTEGER PRIMARY KEY,
                  cnic TEXT UNIQUE,
                  name TEXT,
                  status TEXT DEFAULT 'approved',
                  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def extract_cnic(text):
    """Extract CNIC from email text using regex"""
    matches = re.findall(r'\b\d{5}-\d{7}-\d{1}\b', text)  # Standard CNIC format
    return matches[0] if matches else None

def extract_name(text):
    """Extract name from email text"""
    name_match = re.search(r'(?:name|guest)[:\s-]*([^\n]+)', text, re.IGNORECASE)
    return name_match.group(1).strip() if name_match else "Unknown"

def process_emails():
    """Background thread to check emails and populate database"""
    while True:
        try:
            # Connect to email server (configure these in your .env file)
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
            mail.select('inbox')

            # Search for unread emails with CNIC information
            status, messages = mail.search(None, '(UNSEEN SUBJECT "CNIC")')
            
            if status == 'OK':
                for mail_id in messages[0].split():
                    status, msg_data = mail.fetch(mail_id, '(RFC822)')
                    if status == 'OK':
                        raw_email = msg_data[0][1]
                        email_message = email.message_from_bytes(raw_email)
                        
                        # Get email body text
                        body = ""
                        if email_message.is_multipart():
                            for part in email_message.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = email_message.get_payload(decode=True).decode()
                        
                        # Extract CNIC and name
                        cnic = extract_cnic(body)
                        name = extract_name(body)
                        
                        if cnic:
                            conn = sqlite3.connect(DB_PATH)
                            c = conn.cursor()
                            c.execute('''INSERT OR IGNORE INTO guests (cnic, name)
                                         VALUES (?, ?)''', (cnic, name))
                            conn.commit()
                            conn.close()
                            
                            # Mark email as read
                            mail.store(mail_id, '+FLAGS', '\\Seen')
            
            mail.logout()
            
        except Exception as e:
            print(f"Email processing error: {e}")
        
        time.sleep(60)  # Check every minute

@app.route('/check_cnic', methods=['POST'])
def check_cnic():
    """Check if CNIC exists in database"""
    try:
        data = request.json
        if not data or 'cnic' not in data:
            return jsonify({'error': 'CNIC number is required'}), 400
        
        cnic = data['cnic'].strip()
        if not cnic:
            return jsonify({'error': 'CNIC cannot be empty'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Only check CNIC existence (ignore name)
        c.execute('SELECT 1 FROM guests WHERE cnic = ?', (cnic,))
        exists = c.fetchone() is not None
        
        return jsonify({
            'status': 'approved' if exists else 'not_found',
            'cnic': cnic
        })
        
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/add_guest', methods=['POST'])
def add_guest():
    """Add new guest with CNIC (name optional)"""
    try:
        data = request.json
        if not data or 'cnic' not in data:
            return jsonify({'error': 'CNIC is required'}), 400
        
        cnic = data['cnic'].strip()
        if not cnic:
            return jsonify({'error': 'CNIC cannot be empty'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Insert or ignore duplicates
        c.execute('''
            INSERT OR IGNORE INTO guests (cnic, name)
            VALUES (?, ?)
        ''', (cnic, data.get('name', '')))
        
        conn.commit()
        return jsonify({
            'message': 'Guest added successfully',
            'cnic': cnic,
            'action': 'created' if c.rowcount > 0 else 'already_exists'
        })
        
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/view_guests', methods=['GET'])
def view_guests():
    """View all guests (for debugging)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT cnic, name, added_at FROM guests ORDER BY added_at DESC')
        guests = [{'cnic': row[0], 'name': row[1], 'added_at': row[2]} 
                 for row in c.fetchall()]
        
        return jsonify({
            'count': len(guests),
            'guests': guests
        })
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    
    # Start email processing thread
    email_thread = Thread(target=process_emails, daemon=True)
    email_thread.start()
    
    app.run(host='0.0.0.0', port=5000)