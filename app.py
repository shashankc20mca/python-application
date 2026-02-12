from flask import Flask, render_template_string
import os
import socket
import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Kubernetes Demo App</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            text-align: center;
        }
        .container {
            margin-top: 100px;
        }
        .card {
            background: white;
            color: #333;
            padding: 30px;
            border-radius: 15px;
            width: 400px;
            margin: auto;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.3);
        }
        h1 {
            margin-bottom: 10px;
        }
        .info {
            margin: 10px 0;
            font-size: 18px;
        }
        .button {
            margin-top: 20px;
            padding: 10px 20px;
            border: none;
            background-color: #2a5298;
            color: white;
            border-radius: 8px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #1e3c72;
        }
        .footer {
            margin-top: 30px;
            font-size: 14px;
            opacity: 0.7;
        }
        .badge {
            background: #4CAF50;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🚀 Kubernetes Demo</h1>
            <div class="info"><strong>Pod Name:</strong> {{ hostname }}</div>
            <div class="info"><strong>Server Time:</strong> {{ time }}</div>
            <div class="info"><strong>Status:</strong> <span class="badge">Healthy</span></div>
            <button class="button" onclick="window.location.reload();">Refresh</button>
        </div>
        <div class="footer">
            Running on EKS Fargate with Gateway API
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    hostname = socket.gethostname()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(HTML_TEMPLATE, hostname=hostname, time=current_time)

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
