from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

# ---------- CONFIGURACIÓN DE BASE DE DATOS ----------
DATABASE_URL = os.getenv('DATABASE_URL') 

# Si estás en local, podés setear manualmente:
# DATABASE_URL = "postgresql://usuario:contraseña@host:puerto/nombre_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# ---------- MODELOS ----------
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

class Compra(Base):
    __tablename__ = 'compras'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer)
    nombre_curso = Column(String)
    fecha = Column(String)
    monto = Column(Float)

# Crear las tablas si no existen
Base.metadata.create_all(engine)

# ---------- FLASK ----------
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Servidor Flask con PostgreSQL funcionando correctamente."

# ---------- REGISTRO ----------
@app.route("/register", methods=["POST"])
def register():
    datos = request.get_json()
    username = datos.get('username')
    email = datos.get('email')
    password = datos.get('password')

    if not username or not email or not password:
        return jsonify({'mensaje': 'Faltan datos'}), 400

    session = Session()
    if session.query(Usuario).filter_by(email=email).first():
        session.close()
        return jsonify({'mensaje': 'El email ya está registrado'}), 409

    nuevo_usuario = Usuario(username=username, email=email, password=password)
    session.add(nuevo_usuario)
    session.commit()
    session.close()
    return jsonify({'mensaje': 'Usuario registrado con éxito'}), 200

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    username = datos.get("username")
    password = datos.get("password")

    if not username or not password:
        return jsonify({'mensaje': 'Faltan datos'}), 400

    session = Session()
    usuario = session.query(Usuario).filter_by(username=username, password=password).first()
    session.close()

    if usuario:
        return jsonify({
            'mensaje': 'Inicio de sesión exitoso',
            'usuario': {
                'username': usuario.username,
                'email': usuario.email
            }
        }), 200
    else:
        return jsonify({'mensaje': 'Usuario o contraseña incorrectos'}), 401

# ---------- LISTAR COMPRAS ----------
@app.route('/api/compras', methods=['POST'])
def obtener_compras_usuario():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Falta el nombre de usuario'}), 400

    session = Session()
    user = session.query(Usuario).filter_by(username=username).first()
    if not user:
        session.close()
        return jsonify({'error': 'Usuario no encontrado'}), 404

    compras = session.query(Compra).filter_by(id_usuario=user.id).all()
    session.close()

    compras_list = [
        {
            'nombre_curso': compra.nombre_curso,
            'fecha': compra.fecha,
            'monto': compra.monto
        } for compra in compras
    ]

    return jsonify(compras_list)

# ---------- REGISTRAR COMPRA ----------
@app.route('/api/registrar-compra', methods=['POST'])
def registrar_compra():
    data = request.get_json()
    username = data.get('username')
    nombre_curso = data.get('nombre_curso')
    fecha = data.get('fecha')
    monto = data.get('monto')

    if not all([username, nombre_curso, fecha, monto]):
        return jsonify({'error': 'Faltan datos'}), 400

    session = Session()
    user = session.query(Usuario).filter_by(username=username).first()

    if not user:
        session.close()
        return jsonify({'error': 'Usuario no encontrado'}), 404

    nueva_compra = Compra(
        id_usuario=user.id,
        nombre_curso=nombre_curso,
        fecha=fecha,
        monto=monto
    )
    session.add(nueva_compra)
    session.commit()
    session.close()

    return jsonify({'success': True}), 200

# ---------- INICIO ----------
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
