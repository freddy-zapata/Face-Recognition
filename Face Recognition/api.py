from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
import pickle
import base64
from database import get_db_connection
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Ruta para servir la página web
@app.route("/")
def index():
    return render_template("index.html")  # Servimos el archivo HTML

@app.route("/crud")
def crud():
    return render_template("crud.html")

# Agregar una nueva persona (sin foto)
@app.route("/personas", methods=["POST"])
def add_persona():
    data = request.json

    # Validación de campos
    nombre = data.get("nombre", "").strip()
    apellido = data.get("apellido", "").strip()
    cargo = data.get("cargo", "").strip()

    if not nombre or not apellido or not cargo:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if len(nombre) > 60 or len(apellido) > 60 or len(cargo) > 60:
        return jsonify({"error": "Los campos no deben superar los 60 caracteres"}), 400

    # Insertar en la base de datos
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO personas (nombre, apellido, cargo) VALUES (%s, %s, %s) RETURNING id;", 
                (nombre, apellido, cargo))
    persona_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": persona_id, "message": "Persona agregada"})


# Subir o actualizar la foto de una persona
@app.route("/personas/<int:id>/foto", methods=["PUT"])
def subir_foto(id):
    data = request.json
    foto_b64 = data.get("foto")
    if not foto_b64:
        return jsonify({"error": "No se proporcionó la foto"}), 400

    foto_bin = base64.b64decode(foto_b64)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE personas SET foto = %s WHERE id = %s;", (foto_bin, id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Foto actualizada correctamente"})

# Eliminar persona
@app.route("/personas/<int:id>", methods=["DELETE"])
def delete_persona(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM encodings WHERE id_persona = %s;", (id,))  # Eliminar encodings primero
    cur.execute("DELETE FROM personas WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Persona eliminada"})

# Obtener todas las personas (con foto en base64)
@app.route("/personas", methods=["GET"])
def get_personas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, apellido, cargo, foto FROM personas;")
    personas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        "id": p[0],
        "nombre": p[1],
        "apellido": p[2],
        "cargo": p[3],
        "foto": base64.b64encode(p[4]).decode("utf-8") if p[4] else None
    } for p in personas])

# Guardar un nuevo registro de acceso con foto
@app.route("/accesos", methods=["POST"])
def log_access():
    data = request.json
    foto_binaria = base64.b64decode(data["foto"])  # Convertir Base64 a binario
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO accesos (id_persona, fecha_hora, foto) VALUES (%s, %s, %s);", 
                (data["id_persona"], datetime.now(), foto_binaria))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Acceso registrado"})

# Obtener los accesos, si es conocido foto de la BDD, si es desconocido foto de detección
@app.route("/accesos", methods=["GET"])
def get_accesos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id_persona, p.nombre, p.apellido, p.cargo, a.fecha_hora,
               COALESCE(p.foto, a.foto) as foto_final
        FROM accesos a
        LEFT JOIN personas p ON a.id_persona = p.id
        ORDER BY a.fecha_hora DESC;
    """)
    accesos = cur.fetchall()
    cur.close()
    conn.close()

    resultados = []
    for acc in accesos:
        id_persona, nombre, apellido, cargo, fecha_hora, foto = acc
        resultados.append({
            "nombre": nombre if nombre else "Desconocido",
            "apellido": apellido if apellido else "",
            "cargo": cargo if cargo else "N/A",
            "fecha_hora": fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "foto": base64.b64encode(foto).decode("utf-8") if foto else None
        })
    return jsonify(resultados)


# Servir los archivos estáticos (CSS, JS, imágenes)
app.static_folder = 'static'
app.template_folder = 'templates'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001, debug=True)
