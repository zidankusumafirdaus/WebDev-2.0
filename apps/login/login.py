from flask import Blueprint, render_template, request, redirect, session
from models import User, Admin
from werkzeug.security import check_password_hash
from models import User, Admin

login_bp = Blueprint('login', __name__, template_folder='templates', static_folder='static')

@login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        member = User.get(username=username)
        admin = Admin.getadmin(username=username)
        
        if member and check_password_hash(member.password, password):
            session['loggedin'] = True
            session['username'] = username
            return redirect("/dash")  
            
        elif admin and check_password_hash(admin.password, password):
            session['loggedin'] = True
            session['username'] = username
            return redirect("/dashboardadmin")
        
        if not member and not admin:
            return render_template("login.html", error="User tidak Ditemukan")

        return render_template("login.html", error="Username atau password salah")
    return render_template("login.html")
