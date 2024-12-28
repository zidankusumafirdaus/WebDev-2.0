from flask import Blueprint, render_template, request, redirect, session
from models import User
from werkzeug.security import check_password_hash
from models import User

login_bp = Blueprint('login', __name__, template_folder='templates', static_folder='static')

@login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        member = User.get(username=username)

        if member and check_password_hash(member.password, password):
            session['loggedin'] = True
            session['username'] = username
            session['role'] = member.role  

            
            if member.role == 'superuser':
                return redirect("/dashboardsuper")
            elif member.role == 'admin':
                return redirect("/dashadmin")
            elif member.role == 'user':
                return redirect("/dash")

        return render_template("login.html", error="Username atau password salah")
    return render_template("login.html")
