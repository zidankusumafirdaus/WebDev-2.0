from flask import Blueprint, render_template, session, redirect, url_for, make_response
from auth import login_required, role_required

user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')

@user_bp.route("/dash")
@login_required
@role_required('user','admin','superadmin') #penentu role
def dash():
    username = session.get('username')
    role = session.get('role')
    return render_template("dash.html", username=username, role=role)

@user_bp.route('/logout')
def user_logout():
    """Logout user, clear session, and redirect to login page."""
    session.clear()  # Menghapus seluruh data dari sesi
    
    # Buat respons untuk menghapus cache
    response = make_response(redirect(url_for('login.login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response  # Redirect ke halaman login dengan cache dihapus


# Ndisor iki tambah ono fitur gwe dashboard e user