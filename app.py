from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "mysecretkey")
DB_PATH = os.environ.get("DB_PATH", "appointments.db")

# -------------------------
# Database initialization
# -------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    service TEXT,
                    appointment_datetime TEXT,
                    created_at TEXT
                );''')
    conn.commit()
    conn.close()

# -------------------------
# Add new appointment
# -------------------------
def add_appointment(name, email, phone, service, appointment_datetime):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO appointments 
                (name, email, phone, service, appointment_datetime, created_at)
                VALUES (?, ?, ?, ?, ?, ?)''',
              (name, email, phone, service, appointment_datetime, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        appointment_datetime = request.form.get('appointment_datetime')

        if not name or not appointment_datetime:
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for('book'))

        add_appointment(name, email, phone, service, appointment_datetime)
        flash("Your appointment has been booked successfully!", "success")
        return redirect(url_for('index'))

    return render_template('book.html')

@app.route('/healthz')
def healthz():
    return jsonify(status="ok"), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
