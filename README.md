# CNIC Authenticator

## Overview
CNIC Authenticator is a Python-based application designed to scan and process Computerized National Identity Cards (CNICs) using Optical Character Recognition (OCR). It extracts key details such as CNIC number, name, father’s name, date of birth, gender, and country of stay, then integrates an email-based authentication system to verify and authorize scanned identities. The project uses a modular architecture, combining a GUI for scanning and OCR with a separate Flask server for authentication and database management.

## Features
- **CNIC Scanning**: Captures CNIC images using the A8Capture scanner and processes them with a Python OCR script (`ocr_doctr.py`).
- **OCR Processing**: Extracts structured data (JSON) from CNIC images, including CNIC number, name, and other fields.
- **GUI Interface**: Displays scan status and OCR results in real-time using a `ttkbootstrap`-based interface.
- **Email Authentication**: Sends CNIC details to an admin via email with secure authorization links and QR codes.
- **Database Storage**: Stores CNIC details and authorization status in an SQLite database.

## Project Structure
```
CNIC_Authenticator/
├── Demo.exe                # A8Capture scanner executable
├── wh.jpg                  # Temporary CNIC image (excluded via .gitignore)
├── cnic_ocr_gui.py         # GUI script for scanning and OCR
├── ocr_doctr.py            # OCR processing script
├── cnic_auth_system.py     # Flask server for email authentication and database
├── cnic_database.db        # SQLite database (excluded via .gitignore)
├── A8CaptureEx_X64.dll     # A8Capture SDK DLL for scanner integration
├── README.md               # Project documentation
└── .gitignore              # Excludes temporary files
```

## Requirements
- **Python 3.8+**
- **A8Capture Scanner**: Hardware required for CNIC scanning, with the A8Capture SDK and associated DLL files (e.g., `A8CaptureEx_X64.dll`).
- **Dependencies**:
  ```bash
  pip install ttkbootstrap flask python-doctr qrcode pillow requests
  ```
  - For `python-doctr`, install with TensorFlow or PyTorch:
    ```bash
    pip install python-doctr[tf]
    ```
- **Git for Windows** (for repository management)
- **SMTP Server** (e.g., Gmail with app-specific password)
- **A8Capture SDK**: Ensure the SDK and DLL files (e.g., `A8CaptureEx_X64.dll`) are installed and accessible in the project directory or system path.

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Afsah-Hyder/CNIC_Authenticator.git
   cd CNIC_Authenticator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   - If no `requirements.txt` exists, install packages listed above.

3. **Install A8Capture SDK**:
   - Obtain the A8Capture SDK from the scanner provider.
   - Place the DLL files (e.g., `A8CaptureEx_X64.dll`) in the project directory or a system path (e.g., `C:\Windows\System32`).
   - Ensure `Demo.exe` is configured to use the A8Capture scanner via the SDK.

4. **Configure Email Settings**:
   - Edit `cnic_auth_system.py`:
     ```python
     sender_email = "your_email@example.com"
     password = "your_app_password"  # Use app-specific password for Gmail
     smtp_server = "smtp.gmail.com"
     smtp_port = 587
     ```
   - Alternatively, use environment variables:
     ```bash
     set EMAIL_PASSWORD=your_app_password
     ```
     ```python
     import os
     password = os.getenv("EMAIL_PASSWORD")
     ```

5. **Verify Scanner and Paths**:
   - Connect the A8Capture scanner via USB or Ethernet.
   - Verify paths in `cnic_ocr_gui.py` match your system:
     ```python
     DEMO_PATH = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\bin\Release\Demo.exe'
     WH_PATH = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\wh.jpg'
     OCR_SCRIPT = r'C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo\ocr_doctr.py'
     ```

6. **Run the Application**:
   - Start the Flask authentication server:
     ```bash
     python cnic_auth_system.py
     ```
   - Start the GUI and scanning application:
     ```bash
     python cnic_ocr_gui.py
     ```

## Usage
1. Launch `cnic_ocr_gui.py` to open the GUI.
2. Place a CNIC card in the A8Capture scanner when prompted.
3. The application scans the card, processes it with OCR, and displays extracted details (e.g., CNIC number, name).
4. The Flask server sends an email to the admin with CNIC details and authorization links/QR codes.
5. Admin clicks “Authorize” or “Deny” links to update the SQLite database (`cnic_database.db`).

## Security Notes
- Use environment variables for sensitive data (e.g., email passwords).
- Ensure `.gitignore` excludes temporary files:
  ```
  wh.jpg
  cnic_database.db
  temp_cnic.jpg
  *.pyc
  __pycache__/
  *.exe
  .env
  ```
- Tokens in authorization links are UUID-based for security (consider adding expiration in production).

## Troubleshooting
- **Scanner Errors**: Ensure the A8Capture scanner is connected, and SDK/DLL files are correctly installed.
- **OCR Errors**: Verify `ocr_doctr.py` compatibility and clear CNIC images.
- **Email Issues**: Check SMTP settings and app-specific password.
- **Database Errors**: Confirm SQLite database permissions and schema.

## Contributing
Contributions are welcome! Please submit pull requests or issues to `https://github.com/Afsah-Hyder/CNIC_Authenticator`.

## License
This project is licensed under the MIT License.