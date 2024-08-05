from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def web_application():
    return render_template("index.html")

app.run()

