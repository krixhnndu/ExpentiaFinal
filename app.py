from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Database Connection Function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))

        user = cursor.fetchone()
        
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again!", 401

    return render_template('login.html')
# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return "User already exists, try logging in!", 400
        
        
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    
    return render_template('signup.html')



# Home Route
@app.route('/')
def index():
    return render_template('index.html')


# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')

# Expense Tracker Route
@app.route('/expensetracker')
def expensetracker():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('expensetracker.html')

# User Route for Fetching Username
@app.route('/user')
def get_user():
    if 'username' in session:
        return jsonify({"username": session['username']})
    return jsonify({"error": "Not logged in"}), 401

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
