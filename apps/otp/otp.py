import random
import smtplib
from flask import Blueprint, render_template, request, session, redirect, url_for
from email.message import EmailMessage
from models import User
from dotenv import load_dotenv
import os

load_dotenv()

otp_bp = Blueprint('otp', __name__, template_folder='templates', static_folder='static')

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def code_otp():
    """Generate a 6-digit OTP."""
    otp = "".join(str(random.randint(0, 9)) for _ in range(6))
    return otp

def send_otp(otp_code):
    """Send the OTP to the user's email."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        message = EmailMessage()
        message['Subject'] = 'OTP Verification'
        message['From'] = EMAIL_ADDRESS
        message['To'] = session.get('email')
        message.set_content(f"Your OTP is: {otp_code}")

        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return False

@otp_bp.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form.get("otp")

        # Validasi OTP
        if user_otp == session.get('otp'):
            # Simpan user ke database
            username = session.pop('username', None)
            email = session.pop('email', None)
            password = session.pop('password', None)

            if username and email and password:
                User.create(username=username, password=password, email=email)
                session.pop('otp', None)  
                return redirect(url_for('login.login'))  

        return render_template("otp.html", pesan="Kode OTP salah. Silakan coba lagi.")

    return render_template("otp.html")
