from flask import Blueprint, render_template, session
from auth import login_required, role_required

user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')

@user_bp.route("/dash")
@login_required
@role_required('user','admin','superadmin') #penentu role
def dash():
    username = session.get('username') 
    role = session.get('role')        
    return render_template("dash.html", username=username, role=role)

# Ndisor iki tambah ono fitur gwe dashboard e user