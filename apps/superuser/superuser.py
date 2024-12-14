from flask import Blueprint, render_template
from auth import login_required, role_required

superuser_bp = Blueprint('superuser', __name__, template_folder='templates', static_folder='static')

@superuser_bp.route("/dashboardsuper")
@login_required
@role_required('superuser') #penentu role
def dashboardsuper():
    return render_template("dashboardsuper.html")

# Ndisor iki tambah ono fitur gwe dashboard e superuser