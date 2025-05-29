import sqlite3

# Conectarse a la base de datos
conn = sqlite3.connect('usuarios.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Traer todas las compras
compras = cursor.execute('''
    SELECT compras.id, usuarios.username, compras.nombre_curso, compras.fecha, compras.monto
    FROM compras
    JOIN usuarios ON compras.id_usuario = usuarios.id
    ORDER BY compras.fecha DESC
''').fetchall()

# Mostrar compras
if compras:
    print("Listado de compras:\n")
    for compra in compras:
        print(f"ID: {compra['id']}")
        print(f"Usuario: {compra['username']}")
        print(f"Curso: {compra['nombre_curso']}")
        print(f"Fecha: {compra['fecha']}")
        print(f"Monto: ${compra['monto']}")
        print("-" * 30)
else:
    print("No hay compras registradas.")

conn.close()
