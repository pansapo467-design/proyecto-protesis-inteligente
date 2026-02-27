import asyncio
import requests
from bleak import BleakClient

# Configuración
MAC_ADDRESS = "30:32:45:32:29:01"
# La llave maestra que descubrimos hace un momento
CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
SERVER_URL = "http://127.0.0.1:5000/api/update_biometrics"

def notification_handler(sender, data):
    """Esta función recibe los bytes y los manda al servidor"""
    print(f"📡 Datos crudos: {data.hex()}")
    
    # TRADUCCIÓN INICIAL: 
    # Las pulseras suelen mandar el ritmo en el byte 1 o 2. 
    # Si en tu terminal ves que cambia un número al poner el dedo, ajusta el índice [1]
    try:
        ritmo = data[1] if len(data) > 1 else 70 
        
        # Preparamos el paquete para el servidor
        payload = {
            "ritmo": ritmo,
            "presion": "120/80", # Valor fijo por ahora hasta descifrar el byte
            "oxigeno": 98,
            "temperatura": 36.5
        }
        
        # Enviamos a app.py
        response = requests.post(SERVER_URL, json=payload)
        if response.status_code == 201:
            print(f"✅ Enviado a DB: {ritmo} BPM")
    except Exception as e:
        print(f"❌ Error enviando datos: {e}")

async def main():
    print(f"Buscando pulsera en {MAC_ADDRESS}...")
    async with BleakClient(MAC_ADDRESS) as client:
        if client.is_connected:
            print("¡CONECTADO AL SISTEMA!")
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
            
            # Se queda escuchando indefinidamente
            while True:
                await asyncio.sleep(1)

try:
    asyncio.run(main())
except Exception as e:
    print(f"Conexión perdida: {e}")