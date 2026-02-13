from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
# CORS habilitado para que Lovable pueda comunicarse sin bloqueos
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuración de conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="1779",
        client_encoding='utf-8'
    )

# Middleware para manejar peticiones OPTIONS (CORS) de forma automática
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

@app.route('/')
def index():
    return "Servidor SmartBreast API - Operativo"

# --- 1. RUTA PARA EL DASHBOARD DEL PACIENTE (Juanito) ---
@app.route('/api/paciente/<int:id>', methods=['GET'])
def detalle_paciente(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT nombre FROM usuarios WHERE id = %s", (id,))
        user = cur.fetchone()
        cur.execute("""
            SELECT temperatura, ritmo_cardiaco 
            FROM lecturas_sensores 
            WHERE usuario_id = %s 
            ORDER BY fecha_hora DESC LIMIT 1
        """, (id,))
        sens = cur.fetchone()
        cur.close()
        conn.close()
        
        return jsonify({
            "nombre": user[0] if user else "Usuario",
            "temperatura": float(sens[0]) if sens else 36.5,
            "ritmo": sens[1] if sens else 70
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 2. RUTA PARA EL ESTADO DEL DISPOSITIVO (Batería y Temp Interna) ---
@app.route('/api/estado/<int:id>', methods=['GET'])
def estado_dispositivo(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT nivel_bateria, temp_interna FROM estado_protesis WHERE usuario_id = %s", (id,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        
        return jsonify({
            "bateria": res[0] if res else 100,
            "temp_protesis": float(res[1]) if res else 31.0
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. RUTA PARA LA APP DE DOCTORES (Monitoreo General) ---
@app.route('/api/doctor/monitoreo', methods=['GET'])
def monitoreo_doctor():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, nombre, 'Estable' as estado FROM usuarios WHERE rol = 'paciente'")
        pacientes = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(pacientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 4. RUTA PARA LA AUDITORÍA DEL ASISTENTE VIRTUAL ---
@app.route('/api/ia/auditoria', methods=['POST'])
def guardar_auditoria():
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ai_assistant_audit (usuario_id, consulta_usuario, respuesta_ia)
            VALUES (%s, %s, %s)
        """, (2, data.get('consulta'), data.get('respuesta')))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "Registro de auditoría guardado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 5. RUTA PARA CITAS (Opcional, para el asistente) ---
@app.route('/api/citas/<int:id>', methods=['GET'])
def obtener_citas(id):
    return jsonify([{"fecha": "2026-02-15", "motivo": "Revisión Post-Operatoria"}]), 200

# --- BLOQUE PRINCIPAL (Asegúrate de que 'app.run' tenga sangría) ---
if __name__ == '__main__':
    # Forzamos a que escuche en 127.0.0.1 (IPv4)
    app.run(debug=True, host='127.0.0.1', port=5000)