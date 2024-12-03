from flask import Flask
from apps.register.register import register_bp
from apps.login.login import login_bp
from apps.qr.qr import qr
import models

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(register_bp, url_prefix="/register")
app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(qr, url_prefix="/user")

if __name__ == '__main__':
    models.create_tables()  
    app.run(debug=True)
