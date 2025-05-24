from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.utils import secure_filename
import sqlite3
import os
import datetime

app = Flask(__name__)
app.secret_key = '31f8be965645acd38f5567b2c8b96d5e'
DB_PATH = os.path.join('database', 'database.db')
UPLOAD_FOLDER = os.path.join('static', 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database and admin account
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            bio TEXT DEFAULT '',
            profile_pic TEXT DEFAULT ''
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            image TEXT,
            price REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            course_id INTEGER,
            payment_method TEXT,
            enrollment_time TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            course_id INTEGER
        )
    ''')

    # Add default admin if not exists
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))

    conn.commit()
    conn.close()

# Context processor to expose username to all templates
@app.context_processor
def inject_user_info():
    user = None
    if 'user_id' in session:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE id=?", (session['user_id'],))
        row = c.fetchone()
        if row:
            user = row[0]
        conn.close()
    return dict(logged_in_user=user)

# Home
@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM courses LIMIT 10")
    courses = c.fetchall()
    conn.close()
    return render_template('home.html', courses=courses)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials!"
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM enrollments WHERE user_id=?', (session['user_id'],))
    enrolled_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM courses')
    total_courses = c.fetchone()[0]
    c.execute('''
        SELECT courses.title, enrollments.payment_method, enrollments.enrollment_time
        FROM enrollments
        JOIN courses ON enrollments.course_id = courses.id
        WHERE enrollments.user_id=?
    ''', (session['user_id'],))
    enrolled_courses = c.fetchall()
    conn.close()
    return render_template('dashboard.html', enrolled_count=enrolled_count, total_courses=total_courses, enrolled_courses=enrolled_courses)

# Add Course (Admin Only, with Image Upload)
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()
    conn.close()

    if not user or user[0] != 'admin':
        return "Access Denied: Admins only.", 403

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']

        image_file = request.files.get('image')
        image_filename = ''
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image_file.save(image_path)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO courses (title, description, image, price) VALUES (?, ?, ?, ?)",
                  (title, description, image_filename, price))
        conn.commit()
        conn.close()
        flash('Course added successfully!')
        return redirect(url_for('dashboard'))

    return render_template('add_course.html')

# Courses
@app.route('/courses')
def courses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM courses")
    courses = c.fetchall()
    conn.close()
    return render_template('courses.html', courses=courses)

# Search
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if query:
        c.execute("SELECT * FROM courses WHERE title LIKE ?", ('%' + query + '%',))
    else:
        c.execute("SELECT * FROM courses")
    results = c.fetchall()
    conn.close()
    return render_template('search.html', courses=results, query=query)

# Cart
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT cart.id, courses.title, courses.price, courses.image
        FROM cart
        JOIN courses ON cart.course_id = courses.id
        WHERE cart.user_id=?
    ''', (session['user_id'],))
    cart_items = c.fetchall()
    conn.close()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/add-to-cart/<int:course_id>')
def add_to_cart(course_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO cart (user_id, course_id) VALUES (?, ?)", (session['user_id'], course_id))
    conn.commit()
    conn.close()
    return redirect(url_for('cart'))

@app.route('/remove-from-cart/<int:cart_id>')
def remove_from_cart(cart_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM cart WHERE id=?", (cart_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('cart'))

# Payment Page
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        enrollment_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT course_id FROM cart WHERE user_id=?", (session['user_id'],))
        course_ids = c.fetchall()
        for course_id in course_ids:
            c.execute("INSERT INTO enrollments (user_id, course_id, payment_method, enrollment_time) VALUES (?, ?, ?, ?)",
                      (session['user_id'], course_id[0], payment_method, enrollment_time))
        c.execute("DELETE FROM cart WHERE user_id=?", (session['user_id'],))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))
    return render_template('payment.html')

# Payment Success
@app.route('/success')
def success():
    return render_template('success.html')

# Course Description Popup API
@app.route('/course/<int:course_id>')
def course_description(course_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT title, description FROM courses WHERE id=?", (course_id,))
    course = c.fetchone()
    conn.close()
    return jsonify({'title': course[0], 'description': course[1]})

from chatbot_data import get_bot_response

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.json.get("message", "").lower()
    response = get_bot_response(user_input)
    return jsonify({"response": response})


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5050)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
