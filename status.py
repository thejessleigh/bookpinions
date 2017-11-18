import json

from flask import Flask
app = Flask(__name__)

@app.route("/")
def status():
    return json.dumps({"status": True})
