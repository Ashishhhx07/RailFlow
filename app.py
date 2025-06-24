from flask import Flask, render_template, request, redirect, send_file
import qrcode
import io
import os
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "crowd_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_ticket', methods=['POST'])
def generate_ticket():
    name = request.form['name']
    from_station = request.form['from']
    to_station = request.form['to']
    date = request.form['date']

    ticket_data = f"Name: {name}\nFrom: {from_station}\nTo: {to_station}\nDate: {date}\nTime: {datetime.now().strftime('%H:%M:%S')}"

    img = qrcode.make(ticket_data)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)

    data = load_data()
    if from_station not in data:
        data[from_station] = 0
    data[from_station] += 1
    save_data(data)

    return send_file(buf, mimetype='image/png')

@app.route('/crowd_status')
def crowd_status():
    data = load_data()
    return render_template('crowd.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
