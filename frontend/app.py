from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

API_BASE_URL = "http://backend:8000"

# Rota para a página inicial
@app.route('/')
def home():
    page = 'home'
    return render_template('index.html', page=page)

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')