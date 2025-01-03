from flask import Blueprint, render_template, session, redirect,url_for, make_response
from auth import login_required, role_required

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin_bp.route("/dashadmin")
@login_required
@role_required('admin','superadmin') #penentu role
def dashadmin():
    return render_template("dashadmin.html")


@admin_bp.route('/logout')
def admin_logout():
    """Logout admin, clear session, and redirect to login page."""
    session.clear() 
    response = make_response(redirect(url_for('login.login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response


# Ndisor iki tambah ono fitur gwe dashboard e admin