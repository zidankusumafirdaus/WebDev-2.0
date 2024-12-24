from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime



visitor_logs = ['sample.log']

def index():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    visitor_logs.append({
        'ip': ip_address,
        'user_agent': user_agent,
        'timestamp': timestamp
    })


    return render_template("log analisis/log.html", logs=visitor_logs)