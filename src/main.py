import time
import random
from database import DatabaseManager
from ai.brain import analizar_riesgo_salud

def registrar_lectura_sensor(usuario_id, temp, presion, ritmo):
    """Inserta datos de sensores en PostgreSQL de forma segura."""
    conn = None
    try:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO lecturas_sensores (usuario_id, temperatura, presion, ritmo_cardiaco)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (usuario_id, temp, presion, ritmo))
        conn.commit()
        print(f" [DB] Datos guardados: Temp {temp}°C | Presión {presion} | Ritmo {ritmo}")
        
    except Exception as e:
        print(f" [Error DB]: No se pudo guardar la lectura. {e}")
    finally:
        if conn:
            DatabaseManager.return_connection(conn)

def ejecutar_sistema_monitoreo():
    """Simula el funcionamiento continuo de la prótesis."""
    print("---  SmartBreast: Iniciando Monitoreo Inteligente ---")
    usuario_prueba = 1  # El ID que creamos en pgAdmin

    try:
        # 1. Simular lectura de sensor físico
        # Generamos datos aleatorios realistas
        t_simulada = round(random.uniform(36.0, 39.0), 1)
        p_simulada = random.randint(110, 150)
        r_simulada = random.randint(60, 110)

        # 2. Guardar en la base de datos
        registrar_lectura_sensor(usuario_prueba, t_simulada, p_simulada, r_simulada)

        # 3. Consultar al Asistente IA inmediatamente
        print("\n---  Procesando con IA ---")
        resultado_ia = analizar_riesgo_salud(usuario_prueba)
        print(f"Asistente dice: {resultado_ia}")

    except KeyboardInterrupt:
        print("\n Monitoreo detenido por el usuario.")
    except Exception as e:
        print(f"⚠️ Error inesperado en el sistema: {e}")

if __name__ == "__main__":
    # Ejecutamos una vez para probar. 
    # Si quieres que sea continuo, podrías meterlo en un ciclo 'while True'
    ejecutar_sistema_monitoreo()