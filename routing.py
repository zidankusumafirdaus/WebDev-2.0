from flask import Flask, render_template, request, redirect, session, url_for
from models import User, create_tables, Admin
from config import Config
from werkzeug.security import check_password_hash
from otp import sendotp, codeotp
import qrcode
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)
app.config.from_object(Config)
app.config['kunci'] = '123'


@app.before_request
def setup_database():
    if not hasattr(app, 'first_request'):
        create_tables()
        app.first_request = True


@app.route("/")
def web_application():
    return render_template("web_application/index.html")


@app.route("/register", methods=["GET", "POST"])
def Register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not (username and password and email):
            return render_template("register & otp/register.html", pesan="Form Tidak Boleh Kosong.")
        user_terpakai = User.get(username) or User.get(email=email)
        if user_terpakai:
            return render_template("register & otp/register.html", pesan="Username atau Email Sudah Terpakai.")
        session['data_registrasi'] = {
            'username': username, 'email': email, 'password': password}
        session['email'] = email
        return redirect("/otp")
    return render_template("register & otp/register.html")


@app.route("/registeradmin", methods=["GET", "POST"])
def Registeradmin():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        kunci = request.form.get("kunci")

        if not (username and password and email and kunci):
            return render_template("register & otp/registeradmin.html", pesan="Form Tidak Boleh Kosong.")
        admin_terpakai = Admin.getadmin(
            username) or Admin.getadmin(email=email)
        if admin_terpakai:
            return render_template("register & otp/registeradmin.html", pesan="Username atau Email Sudah Terpakai.")
        if not kunci:
            return render_template("register & otp/registeradmin.html", pesan="Kunci Tidak Boleh Kosong.")
        if kunci.lower() != app.config['kunci']:
            return render_template("register & otp/registeradmin.html", pesan="Kunci Salah.")
        Admin.create(username, password, email)
        session['email'] = email
        Flask('Berhasil Registrasi Sebagai Admin.')
        return redirect("/otp")
    return render_template("register & otp/registeradmin.html")


@app.route("/otp", methods=["GET", "POST"])
def otp():
    if request.method == "POST":
        input_otp = request.form.get('otp')
        if input_otp == session.get('otp'):
            registrasi_take = session.get('data_registrasi')
            if registrasi_take:
                User.create(username = registrasi_take['username'], password = registrasi_take['password'], email = registrasi_take['email'])
                session.pop('data_registrasi', None)
            return redirect('/login')
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

        admin = Admin.getadmin(username)
        member = User.get(username)
        if member and check_password_hash(member.password, password):
            return redirect("/dash")
        elif admin and check_password_hash(admin.password, password):
            return redirect("/dashboardadmin")
        else:
            return render_template('register & otp/login.html', error='username atau password salah')
        
    return render_template('register & otp/login.html')


@app.route("/dash")
def dash():
    return render_template('dashboard/dash.html')

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('level', None)
    return redirect(url_for('web_application'))


@app.route("/dashboardadmin")
def dashboardadmin():
    return render_template("dashboard/dashadmin.html")

@app.route('/barcode')
def barcode():
    return render_template('barcode/barcode.html')

@app.route('/generateQR', methods=['POST'])
def generateQR():
    memory = BytesIO()
    data = request.form.get('link')
    img = qrcode.make(data)
    img.save(memory)
    memory.seek(0)
    
    base64_img = "data:image/png;base64," + b64encode(memory.getvalue()).decode('ascii')
    
    return render_template('barcode/barcode.html', data=base64_img)

if __name__ == "__main__":
    app.run(debug=True)
