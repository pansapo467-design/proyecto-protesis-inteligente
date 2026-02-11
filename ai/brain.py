import os
from src.database import DatabaseManager

def analizar_riesgo_salud(usuario_id):
    """
    Analiza las últimas lecturas para detectar anomalías médicas.
    """
    conn = DatabaseManager.get_connection()
    cursor = conn.cursor()
    
    # Obtenemos la última lectura del sensor de la base de datos
    query = """
        SELECT temperatura, presion, ritmo_cardiaco 
        FROM lecturas_sensores 
        WHERE usuario_id = %s 
        ORDER BY fecha_hora DESC LIMIT 1;
    """
    cursor.execute(query, (usuario_id,))
    lectura = cursor.fetchone()
    DatabaseManager.return_connection(conn)

    if not lectura:
        return "Sin datos suficientes para diagnóstico."

    temp, presion, ritmo = lectura
    alertas = []

    # Lógica de diagnóstico 
    if temp > 37.5:
        alertas.append(f"Fiebre detectada ({temp}°C)")
    if ritmo > 100:
        alertas.append(f"Taquicardia detectada ({ritmo} bpm)")
    if presion > 140:                                           # Simplificado para el ejemplo
        alertas.append("Presión arterial alta")

    if not alertas:
        return "Estado del paciente: Estable. No se detectan anomalías."
    else:
        return f"ALERTA MÉDICA: {', '.join(alertas)}. Se recomienda revisión inmediata."