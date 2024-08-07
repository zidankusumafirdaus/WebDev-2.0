from flask import Flask, render_template, request, redirect, session
from models import User, create_tables
from config import Config
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

@app.before_request
def setup_database():
    if not hasattr(app, 'first_request'):
        create_tables()
        app.first_request = True
    
@app.route("/")
def web_application():
    return render_template("index.html")

@app.route("/register", methods = ["GET","POST"])
def Register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not (username and password and email):
            return render_template("register.html", pesan = "Form Tidak Boleh Kosong.")
        user_terpakai = User.get(username) or User.get(email=email)
        if user_terpakai:
            return render_template("register.html", pesan = "Username atau Email Sudah Terpakai.")
        User.create(username, password, email)
        return redirect("/login")
    return render_template("register & otp/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("register & otp/login.html")

if __name__ == "__main__":
    app.run(debug=True)

