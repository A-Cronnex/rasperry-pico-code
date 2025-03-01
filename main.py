from machine import PWM, Pin, Signal
from picozero import RGBLED
from utilities import convert, uid
from constants import *
from micropython import const
#Inicializar pines del LED

import uos

# Get filesystem statistics for the root directory
stats = uos.statvfs("/")

# Calculate free bytes: f_bavail * f_frsize
free_bytes = stats[3] * stats[1]
print("Free flash memory (bytes):", free_bytes)


import sys
import uasyncio as asyncio
import utime
from time import sleep
import network
import aioble
from aioble import security

#Inicializar clases
import bluetooth

# Inicializar BLE y configurar seguridad
                     # Pairing seguro)



nic = network.WLAN(network.WLAN.IF_STA)
nic.active(True)
current_networks = nic.scan()

rgb = RGBLED(red = RED_PIN, green = GREEN_PIN, blue = BLUE_PIN)

pButton1=Pin(PIN_PB1, Pin.IN, Pin.PULL_UP)
pButton2=Pin(PIN_PB2, Pin.IN, Pin.PULL_UP)

device_info = aioble.Service(GENERIC)

connection = None

#Creación de características
aioble.Characteristic(device_info, bluetooth.UUID(MANUFACTURER_ID), read = True, initial="Aaron's_Rasperry")
aioble.Characteristic(device_info, bluetooth.UUID(MODEL_NUMBER_ID), read = True, initial="1.0")
aioble.Characteristic(device_info, bluetooth.UUID(SERIAL_NUMBER_ID), read = True, initial=uid())
aioble.Characteristic(device_info, bluetooth.UUID(HARDWARE_REVISION_ID), read = True, initial = sys.version)
aioble.Characteristic(device_info, bluetooth.UUID(BLE_VERSION_ID), read = True, initial = "1.0")

remote_service = aioble.Service(GENERIC)

button_characteristic = aioble.Characteristic(remote_service, BUTTON_UUID, notify=True, read=True)

aioble.register_services(remote_service, device_info)

connected = False

#Enviar información que será interpretda en el celular
async def connection_watchdog():
    global connected
    while True:
        if connected:
            try:
                # Enviar paquete vacío cada 3 segundos
                await asyncio.wait_for(connection.ping(), timeout=1)
            except:
                connected = False
        await asyncio.sleep(100000)

async def remote_task():
    while True:
        if not connected:
            print("No se ha conectado")
            await asyncio.sleep_ms(100)
            continue
        if pButton1.value() == 0 and pButton2.value() == 0:
            print("Enviando notificación al celular para identificar su posición")
            rgb.color = (255,255,0)
            button_characteristic.write(b"a")
            button_characteristic.notify(connection, b"a")
        elif pButton1.value() == 0:
            rgb.color = (0,255,255)
            print("Haciendo grabación")
            button_characteristic.write(b"b")
            button_characteristic.notify(connection, b"b")
        elif pButton2.value() == 0:
            print("Llamando a emergencias")
            rgb.color = (255,0,255)
            button_characteristic.write(b"c")
            button_characteristic.notify(connection, b"c")
        else:
            print("No se ha enviado nada de información")
            button_characteristic.write(b"d")
            button_characteristic.notify(connection, b"d")
        await asyncio.sleep_ms(500)

async def periphereal_task():
    global connected, connection
    while True:
        connected = False
        async with await aioble.advertise(
            ADV_INTERNAL_MS,
            name = "Aaron's_Rasperry",
            appearance = BLE_APPEREANCE_GENERIC_REMOTE_CONTROL,
            services = [GENERIC]
        ) as connection:
            
            print("Conectado y vinculado a:", connection.device)
            connected = True
            await connection.disconnected()
            print("disconnected")
            
async def main():
    tasks = [
        asyncio.create_task(remote_task()),
        asyncio.create_task(periphereal_task()),
        asyncio.create_task(connection_watchdog()) 
    ]
    
    await asyncio.gather(*tasks)
        
asyncio.run(main())
            



    