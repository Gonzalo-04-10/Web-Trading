import sqlite3

# Conectarse a la base de datos (usa la misma que los usuarios)
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Crear la tabla de compras si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        nombre_curso TEXT NOT NULL,
        fecha TEXT NOT NULL,
        monto REAL NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
    )
''')

conn.commit()
conn.close()

print("Tabla 'compras' creada correctamente.")
