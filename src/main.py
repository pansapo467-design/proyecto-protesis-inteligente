def registrar_lectura_protesis(usuario_id, temp, presion, ritmo):
    conn = None
    try:
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()

        # PASO SÉNIOR: Verificar si el usuario existe antes de insertar
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        if cursor.fetchone() is None:
            print(f" El usuario {usuario_id} no existe. Creándolo automáticamente...")
            cursor.execute(
                "INSERT INTO usuarios (id, nombre, email, rol) VALUES (%s, %s, %s, %s)",
                (usuario_id, "Usuario Automático", f"usuario{usuario_id}@med.com", "paciente")
            )

        # Ahora sí, insertamos la lectura
        query = """
            INSERT INTO lecturas_sensores (usuario_id, temperatura, presion, ritmo_cardiaco)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (usuario_id, temp, presion, ritmo))
        
        conn.commit()
        print(" Todo en orden. Datos guardados con éxito.")

    except Exception as e:
        print(f" Error detectado: {e}")