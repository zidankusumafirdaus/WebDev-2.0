from flask import Blueprint, render_template, request, session, redirect, url_for
from apps.otp.otp import code_otp, send_otp
from models import User

register_bp = Blueprint('register', __name__, template_folder='templates', static_folder='static')

@register_bp.route("/", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validasi form kosong
        if not (username and email and password):
            return render_template("register.html", pesan="Form tidak boleh kosong.")

        if User.get(username=username) or User.get(email=email):
            return render_template("register.html", pesan="Username atau email sudah terdaftar.")

        # Simpan informasi sementara di session
        session['username'] = username
        session['email'] = email
        session['password'] = password

        otp_code = code_otp()
        session['otp'] = otp_code
        if not send_otp(otp_code):
            return render_template("register.html", pesan="Gagal mengirim OTP, coba lagi.")

        return redirect(url_for('otp.verify_otp')) 

    return render_template("register.html")
