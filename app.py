from flask import Flask
from flask_googlecharts import GoogleCharts

app = Flask(__name__)
app.secret_key = "secret key"