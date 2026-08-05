WIFI_SSID = 'Wokwi-GUEST'
WIFI_PASSWORD = ''

MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'esp32-smart-node-01'

PUBLISH_INTERVAL_MS = 3000

TOPICS = {
    'telemetry': 'building/telemetry',
    'temperature': 'building/temperature',
    'humidity': 'building/humidity',
    'light': 'building/light',
    'motion': 'building/motion',
    'smoke': 'building/smoke',
    'health': 'building/health',
    'availability': 'building/availability',
    'light_control': 'building/light/control',
    'fan_control': 'building/fan/control',
    'light_status': 'building/light/status',
    'fan_status': 'building/fan/status',
}

PINS = {
    'dht': 15,
    'ldr': 34,
    'pir': 13,
    'smoke': 35,
    'relay_light': 18,
    'relay_fan': 19
}

DB_FILE = 'local_database.json'
MAX_DB_RECORDS = 50