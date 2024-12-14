from flask import Blueprint, render_template

error_bp = Blueprint('errorhandlers', __name__, template_folder='templates')

# Error 403 - Forbidden
@error_bp.app_errorhandler(403)
def forbidden_error(e):
    return render_template("403.html"), 403

# Error 404 - Not Found
@error_bp.app_errorhandler(404)
def not_found_error(e):
    return render_template("404.html"), 404

# Error 500 - Internal Server Error
@error_bp.app_errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500
