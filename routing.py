from flask import Flask, render_template, request, redirect, session
from models import User, create_tables
from config import Config
from werkzeug.security import check_password_hash
from otp import sendotp, codeotp

app = Flask(__name__)
app.config.from_object(Config)

@app.before_request
def setup_database():
    if not hasattr(app, 'first_request'):
        create_tables()
        app.first_request = True
    
@app.route("/")
def web_application():
    return render_template("web_application/index.html")

@app.route("/register", methods = ["GET","POST"])
def Register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not (username and password and email):
            return render_template("register & otp/register.html", pesan = "Form Tidak Boleh Kosong.")
        user_terpakai = User.get(username) or User.get(email=email)
        if user_terpakai:
            return render_template("register & otp/register.html", pesan = "Username atau Email Sudah Terpakai.")
        User.create(username, password, email)
        session['email'] = email
        return redirect("/otp")
    return render_template("register & otp/register.html")

@app.route("/otp", methods=["GET", "POST"])
def otp():
    if request.method == "POST":
        input_otp = request.form.get("otp")
        if input_otp == session.get('otp'):
            return redirect("/otp_sukses")
        else:
            return render_template("register & otp/otp.html", pesan="Invalid cuy")

    otp_code = codeotp()
    session['otp'] = otp_code
    sendotp(otp_code)
    return render_template("register & otp/otp.html")

@app.route("/otp_sukses")
def otp_sukses():
    return render_template("register & otp/otp_sukses.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        
        berhasil = User.get(username) and User.get(password)
        if berhasil :
            return redirect("/dashboard")
        else :
            return render_template('register & otp/login.html', error = 'username atau password salah')

    return render_template("register & otp/login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/dash.html")

if __name__ == "__main__":
    app.run(debug=True)