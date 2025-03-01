from bluetooth import UUID
from micropython import const
#Inicializar pines del LED
RED_PIN = 18
GREEN_PIN = 19
BLUE_PIN = 20

#Inicializar pines del botón
PIN_PB1 = 0
PIN_PB2 = 1

GENERIC = UUID(0x1848)

MANUFACTURER_ID = const(0x02A29)
MODEL_NUMBER_ID = const(0x2A24)
SERIAL_NUMBER_ID = const(0X2A25)
HARDWARE_REVISION_ID = const(0x2A26)
BLE_VERSION_ID = const(0x2A28)


BUTTON_UUID = UUID(0x2A6E)
BLE_APPEREANCE_GENERIC_REMOTE_CONTROL = const(384)

ADV_INTERNAL_MS = 250_000

