from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    error = False
    
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                     (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            message = 'Неверный логин или пароль'
            error = True
    
    return render_template('login.html', message=message, error=error)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/users')
def users_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        return 'Доступ запрещен', 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, role FROM users')
    users = cursor.fetchall()
    conn.close()
    
    return render_template('users.html', users=users, form_type='list')

@app.route('/users/new', methods=['GET', 'POST'])
def users_new():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        return 'Доступ запрещен', 403
    
    message = None
    error = False
    
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        email = request.form['email']
        role = request.form['role']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)',
                         (username, password, email, role))
            conn.commit()
            conn.close()
            return redirect(url_for('users_list'))
        except sqlite3.IntegrityError:
            message = 'Пользователь с таким логином уже существует'
            error = True
            conn.close()
    
    return render_template('users.html', form_type='new', message=message, error=error, user={})

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def users_edit(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        return 'Доступ запрещен', 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        
        if request.form.get('password'):
            password = hash_password(request.form['password'])
            cursor.execute('UPDATE users SET username=?, password=?, email=?, role=? WHERE id=?',
                         (username, password, email, role, user_id))
        else:
            cursor.execute('UPDATE users SET username=?, email=?, role=? WHERE id=?',
                         (username, email, role, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('users_list'))
    
    cursor.execute('SELECT id, username, email, role FROM users WHERE id=?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return render_template('users.html', user=user, form_type='edit')

@app.route('/users/delete/<int:user_id>')
def users_delete(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        return 'Доступ запрещен', 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('users_list'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)