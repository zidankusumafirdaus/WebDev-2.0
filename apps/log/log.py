from flask import Flask, render_template, request, Blueprint
from datetime import datetime

log = Blueprint("log", __name__, static_folder="static", template_folder="templates")

visitor_logs = ['sample.log']

@log.route('/log')
def index():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    visitor_logs.append({
        'ip': ip_address,
        'user_agent': user_agent,
        'timestamp': timestamp
    })


    return render_template("log.html", logs=visitor_logs)