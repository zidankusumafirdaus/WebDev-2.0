from flask import Flask, render_template, request, redirect, session, url_for
from config import Config

from datetime import datetime


# List untuk menyimpan jejak pengguna
visitor_logs = ['sample.log']

def index():
    # Mendapatkan informasi pengguna
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Simpan jejak pengguna ke log
    visitor_logs.append({
        'ip': ip_address,
        'user_agent': user_agent,
        'timestamp': timestamp
    })

    # Kirim log ke template untuk ditampilkan
    return render_template("log analisis/log.html", logs=visitor_logs)