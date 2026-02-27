import asyncio
from bleak import BleakClient

address = "30:32:45:32:29:01"

async def run(address):
    async with BleakClient(address) as client:
        print(f"Conectado a: {address}")
        # Esto va a listar TODO lo que la pulsera puede hacer
        for service in client.services:
            print(f"\n[Servicio] {service}")
            for char in service.characteristics:
                print(f"  [Característica] {char.uuid} - Propiedades: {char.properties}")

asyncio.run(run(address))