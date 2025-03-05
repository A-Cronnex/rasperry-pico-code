from machine import PWM, Pin, Signal
from picozero import RGBLED
from utilities import convert, uid
from constants import *
from micropython import const
import requests
import json
import network
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


#Red WLAN
nic = network.WLAN(network.WLAN.IF_STA)
nic.active(True)
current_networks = nic.scan()
wlan_networks = {
    
    "house_network" : {"ssid":"","key":""},
    "college_network": {"ssid":"","key":""}
    
    
    }


rgb = RGBLED(red = RED_PIN, green = GREEN_PIN, blue = BLUE_PIN)

pButton1=Pin(PIN_PB1, Pin.IN, Pin.PULL_UP)
pButton2=Pin(PIN_PB2, Pin.IN, Pin.PULL_UP)

device_info = aioble.Service(GENERIC)

connection = None

#Creación de características
aioble.Characteristic(device_info, bluetooth.UUID(MANUFACTURER_ID), read = True, initial="Aaron's_Raspberry")
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
            rgb.color = convert(0,0,0)
            print(nic.isconnected())
            await asyncio.sleep_ms(100)
            continue
        if pButton1.value() == 0 and pButton2.value() == 0:
            print("Encontrar dispositivo")
            rgb.color = convert(255,255,0)
            code = "a".encode("utf-8")
            button_characteristic.write(code)
            button_characteristic.notify(connection,code)
            print("Value a sent")
        elif pButton1.value() == 0:
            rgb.color = convert(0,255,255)
            print("Haciendo grabación")
            code = "b".encode("utf-8")
            button_characteristic.write(code)
            button_characteristic.notify(connection,code)
            print("Notification sent")
        elif pButton2.value() == 0:
            print("Guardando grabacion")
            rgb.color = convert(255,0,255)
            code = "c".encode("utf-8")
            button_characteristic.write(code)
            button_characteristic.notify(connection, code)
            print("Value sent")
        else:
            print("No se ha enviado nada de información")
            rgb.color = convert(255,255,255)
            code = "d".encode("utf-8")
            button_characteristic.write(code)
            button_characteristic.notify(connection,code)
            print(f"Value {code}")
            
        await asyncio.sleep_ms(500)

async def periphereal_task():
    global connected, connection
    while True:
        connected = False
        async with await aioble.advertise(
            ADV_INTERNAL_MS,
            name = "Aaron's_Raspberry",
            appearance = BLE_APPEREANCE_GENERIC_REMOTE_CONTROL,
            services = [GENERIC]
        ) as connection:
            
            print("Conectado y vinculado a:", connection.device)
            connected = True
            await connection.disconnected()
            print("disconnected")
            
            
async def connect_to_wifi():
    
    if not nic.isconnected():
        nic.connect(wlan_networks["house_network"]["ssid"],wlan_networks["house_network"]["key"])
        

def create_request(command,url,api_endpoint,method):
    
    headers = """\
    {method} /{api_endpoint} HTTP/1.1\r\n
    Content-Type: {content_type}\r\n
    Content-Length: {content_length}\r\n
    Host: {host}\r\n
    Connection: close\r\n
    \r\n"""

    port = 8000

    body = f'{{"command": "{command}"}}'
    print(body)

    body_bytes = body.encode('utf-8')
    header_bytes = headers.format(
        method=method,
        api_endpoint=api_endpoint,
        content_type="application/json",
        content_length=len(body_bytes),
        host=f"{url}:{port}"
    )

    print(header_bytes)
    print(body_bytes)

    payload = header_bytes.encode('utf-8') + body_bytes

    return payload
        
async def send_to_API():
    
    import socket
    
    url = "192.168.50.199"
    addr = socket.getaddrinfo(url,8000)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
    s.connect(addr)
    print("Connected!")
        
        
    while True:
        if not nic.isconnected():
            print("No se ha conectado a la red")
            rgb.color = convert(0,0,0)
            await asyncio.sleep_ms(100)
            continue
        if pButton1.value() == 0 and pButton2.value() == 0:
            print("Encontrar dispositivo")
            rgb.color = convert(255,255,0)
            code = "a".encode("utf-8")
            s.send(create_request("a",url,"api","POST"))
            print("Value a sent")
        elif pButton1.value() == 0:
            rgb.color = convert(0,255,255)
            print("Haciendo grabación")
            code = "b".encode("utf-8")
            s.send(create_request("b",url,"api","POST"))
            print("Notification sent")
        elif pButton2.value() == 0:
            print("Guardando grabacion")
            rgb.color = convert(255,0,255)
            code = "c".encode("utf-8")
            s.send(create_request("c",url,"api","POST"))
            print("Value sent")
        else:
            print("No se ha enviado nada de información")
            rgb.color = convert(255,255,255)
            code = "d".encode("utf-8")
            #s.send(create_request("d",url,"api/command","GET"))
            print(f"Value {code}")
            
        await asyncio.sleep_ms(500)
            
async def main():
    
    await connect_to_wifi() 
    tasks = [
        asyncio.create_task(remote_task()),
        asyncio.create_task(periphereal_task()),
        asyncio.create_task(connection_watchdog())
    ]
    
    
    await send_to_API()
        
    

    await asyncio.gather(*tasks)
    
        
asyncio.run(main())