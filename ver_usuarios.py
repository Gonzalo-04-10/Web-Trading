import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

# Traer todos los usuarios
cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()

# Mostrar resultados
for usuario in usuarios:
    print(usuario)

conn.close()
