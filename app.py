from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app) # Esto permite que tu dashboard de Lovable se conecte sin bloqueos

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# REEMPLAZA: 'tu_usuario', 'tu_password' y 'tu_base_de_datos' con tus datos de pgAdmin4
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tu_password@localhost:5432/tu_base_de_datos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELO DE LA TABLA ---
# Debe coincidir exactamente con la tabla que creamos en pgAdmin4
class SensorReading(db.Model):
    __tablename__ = 'sensor_readings'
    id = db.Column(db.Integer, primary_key=True)
    ritmo_cardiaco = db.Column(db.Integer)
    presion_arterial = db.Column(db.String(20))
    oxigeno = db.Column(db.Integer)
    temperatura = db.Column(db.Float)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

# --- RUTA PARA RECIBIR DATOS DE LA PULSERA ---
@app.route('/api/update_biometrics', methods=['POST'])
def update_biometrics():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    try:
        # Creamos el nuevo registro con los datos que vienen del pulsera.py
        nueva_lectura = SensorReading(
            ritmo_cardiaco=data.get('ritmo'),
            presion_arterial=data.get('presion'),
            oxigeno=data.get('oxigeno'),
            temperatura=data.get('temperatura')
        )
        
        db.session.add(nueva_lectura)
        db.session.commit()
        
        print(f"✅ Dato guardado: Ritmo {data.get('ritmo')} BPM")
        return jsonify({"status": "success", "message": "Datos guardados en PostgreSQL"}), 201
    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al guardar: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- RUTA PARA QUE EL DASHBOARD LEA LOS DATOS ---
@app.route('/api/get_latest', methods=['GET'])
def get_latest():
    try:
        # Obtenemos los últimos 20 registros para la gráfica
        readings = SensorReading.query.order_by(SensorReading.fecha_registro.desc()).limit(20).all()
        results = [
            {
                "id": r.id,
                "ritmo": r.ritmo_cardiaco,
                "presion": r.presion_arterial,
                "oxigeno": r.oxigeno,
                "temperatura": r.temperatura,
                "fecha": r.fecha_registro.strftime('%H:%M:%S')
            } for r in readings
        ]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Usamos host='0.0.0.0' para que sea visible en la red del concurso
    app.run(host='0.0.0.0', port=5000, debug=True)