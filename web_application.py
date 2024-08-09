from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

@app.route("/")
def web_application():
    return render_template("web_application/index.html")