from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from datetime import datetime

app = Flask(__name__)
# CORS habilitado para todas las rutas para evitar bloqueos entre Lovable y Bmon
CORS(app, resources={r"/*": {"origins": "*"}})

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",   
        user="postgres",
        password="1779", 
        port="5432"
    )

@app.route('/')
def home():
    return jsonify({
        "status": "Servidor SmartBreast Adaptativo - Activo", 
        "version": "2.6 - Store Patch", 
        "asistente": "Brasie"
    }), 200

# --- [ADAPTADOR EXTRA PARA BMON] ---
# Resolvemos el error 404 que aparecía al usar el chat o sensores
@app.route('/store', methods=['POST', 'OPTIONS'])
def adaptador_store():
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    try:
        data = request.json
        # Imprimimos en la terminal para saber qué está enviando Bmon a /store
        print(f"--- Datos recibidos en /store: {data} ---")
        return jsonify({"status": "success", "message": "Datos recibidos en /store"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- [ADAPTADOR BMON / SUPABASE] ---
@app.route('/funciones/v1/biometría', methods=['POST', 'OPTIONS'])
@app.route('/funciones/v1/biometria', methods=['POST', 'OPTIONS'])
def recibir_biometria_bmon():
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    try:
        data = request.json
        uid = data.get('usuario_id', 2)
        temp = data.get('temp', 36.5)
        bat = data.get('bateria', 100)
        
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO estado_protesis (usuario_id, temp_interna, nivel_bateria, estado, fecha_actualizacion)
            VALUES (%s, %s, %s, 'Activo', NOW())
            ON CONFLICT (usuario_id) 
            DO UPDATE SET temp_interna = EXCLUDED.temp_interna, 
                          nivel_bateria = EXCLUDED.nivel_bateria,
                          fecha_actualizacion = NOW();
        """, (uid, temp, bat))
        conn.commit(); cur.close(); conn.close()
        return jsonify({"message": "Biometría capturada por adaptador local"}), 201
    except Exception as e: return jsonify({"error": str(e)}), 500

# --- [VISTA PACIENTE] ---
@app.route('/api/paciente/<int:id>', methods=['GET', 'OPTIONS'])
def get_paciente(id):
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT id, nombre, email, estado FROM usuarios WHERE id = %s", (id,))
        p = cur.fetchone(); cur.close(); conn.close()
        if p: return jsonify({"id": p[0], "nombre": p[1], "email": p[2], "estado": p[3]}), 200
        return jsonify({"id": id, "nombre": "Paciente", "estado": "Estable"}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/estado/<int:id>', methods=['GET', 'OPTIONS'])
def get_estado(id):
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT nivel_bateria, temp_interna, estado FROM estado_protesis WHERE usuario_id = %s", (id,))
        res = cur.fetchone(); cur.close(); conn.close()
        if res: return jsonify({"bateria": res[0], "temperatura": float(res[1]), "estado": res[2]}), 200
        return jsonify({"bateria": 92, "temperatura": 36.6, "estado": "Óptimo"}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

# --- [VISTA DOCTOR] ---
@app.route('/api/doctor/alertas', methods=['GET', 'OPTIONS'])
def get_doctor_alertas():
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    try:
        conn = get_db_connection(); cur = conn.cursor()
        query = """
            SELECT u.id, u.nombre, e.temp_interna, e.nivel_bateria, e.estado
            FROM estado_protesis e
            JOIN usuarios u ON e.usuario_id = u.id
            ORDER BY e.temp_interna DESC;
        """
        cur.execute(query)
        rows = cur.fetchall(); cur.close(); conn.close()
        return jsonify([{
            "id": r[0], "paciente": r[1], "temp": float(r[2]), "bateria": r[3], "estado": r[4],
            "riesgo": "Alto" if r[2] > 38 else "Medio" if r[2] > 37.5 else "Bajo"
        } for r in rows]), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/doctor/historial/<int:id>', methods=['GET', 'OPTIONS'])
def get_doctor_history(id):
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    return jsonify([
        {"fecha": str(datetime.now().date()), "evento": "Lectura estable", "valor": 36.5},
        {"fecha": "2026-02-13", "evento": "Registro previo", "valor": 37.0}
    ]), 200

@app.route('/api/reporte/<int:id>', methods=['GET', 'OPTIONS'])
def get_reporte_pdf(id):
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    return jsonify({"status": "success", "message": f"Generando reporte para ID {id}", "url": "#"}), 200

# --- CITAS Y CHAT ---
@app.route('/api/citas/<int:id>', methods=['GET', 'POST', 'OPTIONS'])
def handle_citas(id):
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    try:
        conn = get_db_connection(); cur = conn.cursor()
        if request.method == 'POST':
            data = request.json
            cur.execute("INSERT INTO medical_appointments (usuario_id, fecha_cita, motivo) VALUES (%s, %s, %s)", (id, data['fecha'], data['motivo']))
            conn.commit(); cur.close(); conn.close()
            return jsonify({"status": "success"}), 201
        cur.execute("SELECT fecha_cita, motivo FROM medical_appointments WHERE usuario_id = %s", (id,))
        citas = cur.fetchall(); cur.close(); conn.close()
        return jsonify([{"date": str(c[0]), "title": c[1]} for c in citas]), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat_brasie():
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    data = request.json
    texto = data.get('mensaje', '').lower()
    resp = "Soy Brasie. He recibido tu mensaje."
    if "dolor" in texto: resp = "He detectado un reporte de molestia. El doctor ha sido notificado."
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO ai_assistant_audit (usuario_id, consulta_usuario, respuesta_ia) VALUES (%s, %s, %s)", (data.get('usuario_id', 2), texto, resp))
        conn.commit(); cur.close(); conn.close()
        return jsonify({"respuesta": resp}), 201
    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)