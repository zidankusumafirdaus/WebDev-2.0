from flask import Flask, render_template, request, redirect, session, url_for
from models import User, create_tables, Admin
from config import Config
from werkzeug.security import check_password_hash
from otp import sendotp, codeotp
from register import regis_admin
import qrcode
from io import BytesIO
from base64 import b64encode
from flask_socketio import SocketIO, send, join_room, leave_room
from datetime import datetime
from qr import generate_qr

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.before_request
def setup_database():
    if not hasattr(app, 'first_request'):
        create_tables()
        app.first_request = True


@app.route("/")
def web_application():
    return render_template("web_application.html")


@app.route("/register", methods=["GET", "POST"])
def Register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not (username and password and email):
            return render_template("register.html", pesan="Form Tidak Boleh Kosong.")
        user_terpakai = User.get(username) or User.get(email=email)
        if user_terpakai:
            return render_template("register.html", pesan="Username atau Email Sudah Terpakai.")
        session['data_registrasi'] = {
            'username': username, 'email': email, 'password': password}
        session['email'] = email
        session['username'] = username
        
        return redirect("/otp")
    return render_template("register.html")


@app.route("/registeradmin", methods=["GET", "POST"])
def Registeradmin():
    return regis_admin()


@app.route("/otp", methods=["GET", "POST"])
def otp():
    if request.method == "POST":
        input_otp = request.form.get('otp')
        if input_otp == session.get('otp'):
            registrasi_take = session.get('data_registrasi')
            registrasi_admin = session.get('data_admin')
            if registrasi_take:
                User.create(username = registrasi_take['username'], password = registrasi_take['password'], email = registrasi_take['email'])
                session.pop('data_registrasi', None)
            if registrasi_admin:
                Admin.create(username = registrasi_admin['username'], password = registrasi_admin['password'], email = registrasi_admin['email'])
                session.pop('data_admin', None)
            return redirect('/dash')
        else:
            return render_template("otp.html", pesan="Invalid cuy")

    otp_code = codeotp()
    session['otp'] = otp_code
    sendotp(otp_code)
    return render_template("otp.html")


@app.route("/otp_sukses")
def otp_sukses():
    return render_template("otp_sukses.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.getadmin(username)
        member = User.get(username)
        if member and check_password_hash(member.password, password):
            session['loggedin'] = True
            session['username'] = username  
            return redirect("/dash")
        elif admin and check_password_hash(admin.password, password):
            session['loggedin'] = True
            session['username'] = username
            return redirect("/dashboardadmin")
        else:
            return render_template('login.html', error='username atau password salah')
        
    return render_template('login.html')
@app.route("/dash")
def dash():
    return render_template('dash.html')

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('level', None)
    return redirect(url_for('web_application'))


@app.route("/dashboardadmin")
def dashboardadmin():
    return render_template("dashadmin.html")

@app.route('/barcode')
def barcode():
    return render_template('barcode/barcode.html')

@app.route('/generateQR', methods=['POST'])
def generateQR():
    return generate_qr()

@socketio.on('message')
def handle_message(data):
    print(f"Menerima pesan dari {data['username']}: {data['message']}")
    if data['message'] != "User terhubung!":
        timestamp = datetime.now().strftime("%H:%M")
        send({
            'timestamp': timestamp,
            'username': data['username'],
            'text': data['message']
        }, broadcast=True)

@app.route('/chat')
def chat():
    username = session.get('username')
    return render_template('chat.html', username=username)

@socketio.on('connect')
def on_connect():
    print('User Connected')

@socketio.on('disconnect')
def on_disconnect():
    print('User Disconnected')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)

if __name__ == "__main__":
    socketio.run(app, debug=True)
