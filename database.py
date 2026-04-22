import sqlite3
import hashlib

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')

    admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
    user_password = hashlib.sha256('user123'.encode()).hexdigest()

    try:
        cursor.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)', 
                     ('admin', admin_password, 'admin@example.com', 'admin'))
        cursor.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)', 
                     ('user', user_password, 'user@example.com', 'user'))
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()
    print("База данных создана. Пользователи: admin/admin123, user/user123")

if __name__ == '__main__':
    create_database()