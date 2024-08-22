from flask import Flask, render_template, request, redirect, session
from models import Admin

def regis_admin():
    if request.method == 'POST':
        kunci_admin = '123'
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        kunci = request.form.get("kunci")
        admin_terpakai = Admin.getadmin(username) or Admin.getadmin(email=email)
        
        if admin_terpakai:
            return render_template("registeradmin.html", pesan="Username atau Email Sudah Terpakai.")
        if kunci.lower() != kunci_admin:
            return render_template("registeradmin.html", pesan="Kunci Salah.")
        session['data_admin'] = {'username': username, 'email': email, 'password': password}
        return redirect("/otp")
    return render_template("registeradmin.html")