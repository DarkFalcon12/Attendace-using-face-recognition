from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

data_file = 'data/attendance.json'

@app.route('/')
def index():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    dates = sorted(data.keys())
    return render_template('index.html', dates=dates)

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    name = request.form['name']
    date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    late_time = datetime.strptime(current_time, '%H:%M:%S') - datetime.strptime("08:00:00", "%H:%M:%S")

    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    if date not in data:
        data[date] = []

    if not any(entry['name'] == name for entry in data[date]):
        if datetime.now().time() <= datetime.strptime("08:00:00", "%H:%M:%S").time():
            status = "Present"
        else:
            status = f"Late by {late_time}"

        data[date].append({'name': name, 'time': current_time, 'status': status})

        with open(data_file, 'w') as f:
            json.dump(data, f)

        return ('', 204)
    else:
        return ('', 409)

@app.route('/get_attendance')
def get_attendance():
    date = request.args.get('date')
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    
    attendance = data.get(date, [])
    return jsonify(attendance)

if __name__ == '__main__':
    app.run(debug=True)
