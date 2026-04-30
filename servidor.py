import sqlite3
import bcrypt
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
DB_NAME = "tareas.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña_hash TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            título TEXT NOT NULL,
            descripción TEXT,
            completada BOOLEAN DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    conn.commit()
    conn.close()


@app.route("/registro", methods=["POST"])
def registro():
    data = request.get_json()

    if not data or "usuario" not in data or "contraseña" not in data:
        return jsonify({"error": "Faltan usuario o contraseña"}), 400

    usuario = data["usuario"]
    contraseña = data["contraseña"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "El usuario ya existe"}), 409

    contraseña_hash = bcrypt.hashpw(contraseña.encode("utf-8"), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO usuarios (usuario, contraseña_hash) VALUES (?, ?)",
        (usuario, contraseña_hash)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Usuario creado exitosamente"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "usuario" not in data or "contraseña" not in data:
        return jsonify({"error": "Faltan usuario o contraseña"}), 400

    usuario = data["usuario"]
    contraseña = data["contraseña"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, contraseña_hash FROM usuarios WHERE usuario = ?",
        (usuario,)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    if bcrypt.checkpw(contraseña.encode("utf-8"), user["contraseña_hash"]):
        return jsonify({"mensaje": "Login exitoso", "usuario_id": user["id"]}), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401


@app.route("/")
def index():
    from flask import redirect
    return redirect("/tareas")


@app.route("/tareas", methods=["GET"])
def tareas():
    return render_template("index.html"), 200


@app.route("/tareas/<int:usuario_id>", methods=["GET"])
def get_tareas(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, título, descripción, completada FROM tareas WHERE usuario_id = ?",
        (usuario_id,)
    )
    tareas = cursor.fetchall()
    conn.close()
    return jsonify({
        "tareas": [
            {"id": t["id"], "titulo": t["título"], "descripcion": t["descripción"], "completada": bool(t["completada"])}
            for t in tareas
        ]
    }), 200


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    data = request.get_json()
    if not data or "usuario_id" not in data or "titulo" not in data:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tareas (usuario_id, título, descripción) VALUES (?, ?, ?)",
        (data["usuario_id"], data["titulo"], data.get("descripcion", ""))
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Tarea creada"}), 201


@app.route("/tareas/<int:tarea_id>", methods=["PUT"])
def completar_tarea(tarea_id):
    data = request.get_json()
    if not data or "usuario_id" not in data:
        return jsonify({"error": "Falta usuario_id"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tareas SET completada = 1 WHERE id = ? AND usuario_id = ?",
        (tarea_id, data["usuario_id"])
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Tarea completada"}), 200


@app.route("/tareas/<int:tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    usuario_id = request.args.get("usuario_id")
    if not usuario_id:
        return jsonify({"error": "Falta usuario_id"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = ? AND usuario_id = ?", (tarea_id, usuario_id))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Tarea eliminada"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)