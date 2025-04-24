from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'tuba_secret'

# Load attendance data
def load_data():
    try:
        with open('attendance_data.json', 'r') as f:
            return json.load(f)
    except:
        return {}

# Save attendance data
def save_data(data):
    with open('attendance_data.json', 'w') as f:
        json.dump(data, f)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    role = request.form['role']
    session['user'] = username
    session['role'] = role
    return redirect(url_for('dashboard')) if role == 'admin' else redirect(url_for('student'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    data = load_data()
    if request.method == 'POST':
        name = request.form['student']
        status = request.form['status']
        data[name] = status
        save_data(data)
    return render_template('dashboard.html', data=data)

@app.route('/student')
def student():
    data = load_data()
    return render_template('student.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)