from flask import Blueprint, render_template
from auth import login_required, role_required

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin_bp.route("/dashadmin")
@login_required
@role_required('admin','superadmin') #penentu role
def dashboardsuper():
    return render_template("dashadmin.html")

# Ndisor iki tambah ono fitur gwe dashboard e admin