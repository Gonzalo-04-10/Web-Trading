from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3 

app = Flask(__name__)
CORS(app)

def conectar_db():
    return sqlite3.connect("usuarios.db")

# Ruta de prueba para verificar si funciona
@app.route("/")
def home():
    return "Servidor Flask funcionando"

usuarios_registrados = []  # Por ahora los guardamos en memoria



# Ruta para registrar usuarios
@app.route("/register", methods=["POST"])
def register():
    
    datos = request.get_json()

    username = datos.get('username')
    email = datos["email"]
    password = datos["password"]

    if not username or not email or not password:
        return jsonify({'mensaje': 'Faltan datos'}), 400
    
    conn = conectar_db()
    cursor = conn.cursor()

    # Validar si ya existe ese email
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    existe = cursor.fetchone()
    if existe:
        conn.close()
        return jsonify({"mensaje": "El email ya está registrado"}), 409
    
    cursor.execute(
            "INSERT INTO usuarios (username, email, password) VALUES (?, ?, ?)",
            (username, email, password),
        )
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Usuario registrado con éxito"}), 200



# Ruta para iniciar usuarios
@app.route("/login", methods=["POST"])

def login():
    datos = request.get_json()
    username = datos.get("username")
    password = datos.get("password")

    if not username or not password:
        return jsonify({'mensaje': 'Faltan datos'}), 400

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM usuarios WHERE username = ? AND password = ?", (username, password))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return jsonify({
            'mensaje': 'Inicio de sesión exitoso',
            'usuario': {
                'username': usuario[0],
                'email': usuario[1]
            }
        }), 200
    else:
        return jsonify({'mensaje': 'Usuario o contraseña incorrectos'}), 401



#Ruta para buscar compras del usuario
@app.route('/api/compras', methods=['POST'])
def obtener_compras_usuario():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Falta el nombre de usuario'}), 400

    def conectar_db():
        conn = sqlite3.connect('usuarios.db')
        conn.row_factory = sqlite3.Row
        return conn
    conn = conectar_db()

    # Buscar el usuario
    user = conn.execute('SELECT id FROM usuarios WHERE username = ?', (username,)).fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'Usuario no encontrado'}), 404

    user_id = user['id']

    # Traer compras del usuario
    compras = conn.execute('SELECT nombre_curso, fecha, monto FROM compras WHERE id_usuario = ?',(user_id,)).fetchall()
    conn.close()

    # Convertir a lista de diccionarios
    compras_list = [dict(compra) for compra in compras]

    return jsonify(compras_list)


@app.route('/api/registrar-compra', methods=['POST'])
def registrar_compra():
    data = request.get_json()

    username = data.get('username')
    nombre_curso = data.get('nombre_curso')
    fecha = data.get('fecha')
    monto = data.get('monto')

    if not all([username, nombre_curso, fecha, monto]):
        return jsonify({'error': 'Faltan datos'}), 400

    conn = conectar_db()
    cursor = conn.cursor()

    # Buscar ID del usuario
    cursor.execute('SELECT id FROM usuarios WHERE username = ?', (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({'error': 'Usuario no encontrado'}), 404

    id_usuario = user[0]


    # Insertar compra
    try:
        cursor.execute('''
            INSERT INTO compras (id_usuario, nombre_curso, fecha, monto)
            VALUES (?, ?, ?, ?)
        ''', (id_usuario, nombre_curso, fecha, monto))
        conn.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        print('Error al registrar compra:', e)
        return jsonify({'error': 'Error al registrar compra'}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    from os import getenv
    port = int(getenv('PORT', 5000))  # Railway te da el puerto por variable de entorno
    app.run(host='0.0.0.0', port=port)
