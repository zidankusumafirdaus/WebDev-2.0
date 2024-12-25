import os
import json
import qrcode
from flask_bcrypt import Bcrypt
from flask import request, render_template, Blueprint, send_from_directory

qr = Blueprint("qr", __name__, static_folder="static", template_folder="templates")
bcrypt = Bcrypt()

FolderUploads = './apps/qr/uploads'
os.makedirs(FolderUploads, exist_ok=True)

@qr.route('/barcode', methods=['GET', 'POST'])
def barcode():
    if request.method == 'POST':
        if 'link' in request.form:
            # QR Code For URL
            link = request.form['link']
            QRGenerate = qrcode.make(link)
            
            safe_link = bcrypt.generate_password_hash(link.encode()).decode('utf-8') 
            qrSave = os.path.join(FolderUploads, f"{safe_link}.png")
            QRGenerate.save(qrSave)
            return render_template('qr.html', data=f"{safe_link}.png", countries=countries)
        
        elif 'WANumber' in request.form and 'WAText' in request.form:
            # QR Code For WhatsApp
            country_code = request.form.get('CodeCountry')
            WANumber = request.form['WANumber']
            WAMessage = request.form['WAText']

            WhatsAppURL = f"https://wa.me/{country_code}{WANumber}?text={WAMessage}"
            QRGenerate = qrcode.make(WhatsAppURL)
            
            safe_link = bcrypt.generate_password_hash(WhatsAppURL.encode()).decode('utf-8') 
            qrSave = os.path.join(FolderUploads, f"{safe_link}.png")
            QRGenerate.save(qrSave)
            return render_template('qr.html', data=f"{safe_link}.png", countries=countries)

        elif 'GmailAddress' in request.form and 'GmailSubject' in request.form and 'GmailText' in request.form:
            # QR Code For Gmail
            GmailAddress = request.form['GmailAddress']
            GmailSubject = request.form['GmailSubject']
            GmailText = request.form['GmailText']

            GmailURL = f"MATMSG:TO:{GmailAddress};SUB:{GmailSubject};BODY:{GmailText}"
            QRGenerate = qrcode.make(GmailURL)

            safe_link = bcrypt.generate_password_hash(GmailURL.encode()).decode('utf-8')
            qrSave = os.path.join(FolderUploads, f"{safe_link}.png")
            QRGenerate.save(qrSave)
            return render_template('qr.html', data=f"{safe_link}.png", countries=countries)
    return render_template('qr.html', data=None, countries=countries)

@qr.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(FolderUploads, filename)

# Load country codes from JSON file
with open('apps/qr/CountryCodes.json') as f:
    countries = json.load(f)