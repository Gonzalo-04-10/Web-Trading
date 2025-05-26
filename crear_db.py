import sqlite3

def crear_bd():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos y tabla 'usuarios' creadas correctamente.")

if __name__ == '__main__':
    crear_bd()
