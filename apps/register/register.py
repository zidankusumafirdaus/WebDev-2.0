from flask import Blueprint, render_template, request, redirect, session
from models import User

register_bp = Blueprint('register', __name__, template_folder='templates', static_folder='static')

@register_bp.route("/", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not (username and password and email):
            return render_template("register.html", pesan="Form Tidak Boleh Kosong.")
        
        user_terpakai = User.get(username=username) or User.get(email=email)
        if user_terpakai:
            return render_template("register.html", pesan="Username atau Email Sudah Terpakai.")
        
        User.create(username=username, password=password, email=email)
        session['username'] = username
        session['email'] = email

        return redirect("/otp") 
    return render_template("register.html")
