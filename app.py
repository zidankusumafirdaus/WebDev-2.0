from flask import Flask
from apps.register.register import register_bp
from apps.login.login import login_bp
from apps.superuser.superuser import superuser_bp
from apps.admin.admin import admin_bp
from apps.user.user import user_bp
from apps.erorhandlers.erorhandlers import error_bp
from apps.qr.qr import qr
from apps.log.log import log
from apps.otp.otp import otp_bp

import models

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

app.register_blueprint(register_bp, url_prefix="/register")
app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(superuser_bp, url_prefix="/superuser")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(user_bp, url_prefix="/user") 
app.register_blueprint(error_bp)
app.register_blueprint(qr, url_prefix="/qr")
app.register_blueprint(log, url_prefix="/log")
app.register_blueprint(otp_bp, url_prefix="/otp")

if __name__ == '__main__':
    models.create_tables()
    models.initialize_superuser()
    app.run(debug=True)
