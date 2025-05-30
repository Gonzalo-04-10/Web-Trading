from sqlalchemy import create_engine, text
import os

# Lee la URL de conexión a PostgreSQL desde las variables de entorno (Railway la pone ahí)
DATABASE_URL = "postgresql://postgres:tHScDWqYrzfljAJzyJylGjNbeIEQxlIm@shuttle.proxy.rlwy.net:18877/railway"

# Conecta a la base de datos
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # CREA LA TABLA DE USUARIOS
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    '''))

    # CREA LA TABLA DE COMPRAS
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS compras (
            id SERIAL PRIMARY KEY,
            id_usuario INTEGER NOT NULL,
            nombre_curso TEXT NOT NULL,
            fecha TEXT NOT NULL,
            monto REAL NOT NULL
            -- Si Railway te deja más adelante, podés agregar: , FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        );
    '''))

    print("Tablas creadas con éxito.")
