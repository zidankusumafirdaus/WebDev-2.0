from flask import Blueprint, render_template, session, redirect, url_for
from auth import login_required, role_required

superuser_bp = Blueprint('superuser', __name__, template_folder='templates', static_folder='static')

@superuser_bp.route("/dashboardsuper")
@login_required
@role_required('superuser') #penentu role
def dashboardsuper():
    username = session.get('username')
    role = session.get('role')
    return render_template("dashboardsuper.html", username=username, role=role)

@superuser_bp.route('/logout')
def superuser_logout():
    """Logout user and clear session."""
    session.clear()  # Menghapus seluruh data dari session
    return redirect(url_for('login.login'))  # Redirect ke halaman login

# Ndisor iki tambah ono fitur gwe dashboard e superuser