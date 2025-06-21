from flask import Flask, render_template, request, redirect, session, flash, url_for
from mysql.connector import Error, IntegrityError
from database import get_db_connection

app = Flask(__name__)
app.secret_key = 'AEIOU&*^786'  

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials', 'error')
        except Error as e:
            flash(f'Database error: {e}', 'error')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, role, password) VALUES (%s, %s, %s, %s)",
                           (name, email, role, password))
            conn.commit()
            conn.close()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            flash('User already exists', 'error')
        except Error as e:
            flash(f'Database error: {e}', 'error')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    return render_template('home.html', name=session.get('user_name'))


if __name__ == '__main__':
    app.run(debug=True)
