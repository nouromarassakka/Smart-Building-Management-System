import time
import json
import network
from machine import Pin

from config import (
    WIFI_SSID,
    WIFI_PASSWORD,
    MQTT_CLIENT_ID,
    MQTT_BROKER,
    MQTT_PORT,
    TOPICS,
    PINS,
    PUBLISH_INTERVAL_MS,
    DB_FILE,
    MAX_DB_RECORDS
)
from sensors import Sensors
from mqtt_client import MQTTClientWrapper
from database import LocalDatabase

relay_light = Pin(PINS['relay_light'], Pin.OUT, value=0)
relay_fan = Pin(PINS['relay_fan'], Pin.OUT, value=0)

mqtt = None

def calculate_health_score(data):
    score = 100
    temp = data.get('temperature')
    smoke = data.get('smoke')
    
    if temp and temp > 40:
        score -= (temp - 40) * 3
    if smoke == 1:
        score -= 40
        
    return max(0, int(score))

def update_relay(relay_pin, state, status_topic):
    val = 1 if state == "ON" else 0
    relay_pin.value(val)
    if mqtt:
        mqtt.publish(status_topic, "ON" if val else "OFF")

def on_mqtt_message(topic, msg):
    t = topic.decode() if isinstance(topic, bytes) else topic
    p = msg.decode().strip().upper() if isinstance(msg, bytes) else str(msg).upper()
    print("MQTT Command ->", t, p)

    if t == TOPICS["light_control"]:
        update_relay(relay_light, p, TOPICS["light_status"])
    elif t == TOPICS["fan_control"]:
        update_relay(relay_fan, p, TOPICS["fan_status"])

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi:', WIFI_SSID)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 0
        while not wlan.isconnected() and timeout < 20:
            time.sleep(0.5)
            timeout += 1
    if wlan.isconnected():
        print('WiFi Connected! IP:', wlan.ifconfig()[0])
        return True
    print('WiFi Connection Failed!')
    return False

def main():
    global mqtt
    
    connect_wifi()

    sensors = Sensors(
        dht_pin=PINS['dht'],
        ldr_pin=PINS['ldr'],
        pir_pin=PINS['pir'],
        smoke_pin=PINS['smoke']
    )
    db = LocalDatabase(filename=DB_FILE, max_records=MAX_DB_RECORDS)
    
    mqtt = MQTTClientWrapper(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    mqtt.set_callback(on_mqtt_message)
    
    if mqtt.connect():
        mqtt.subscribe(TOPICS["light_control"])
        mqtt.subscribe(TOPICS["fan_control"])
        mqtt.publish(TOPICS["availability"], "Online")

    last_publish = time.ticks_ms() - PUBLISH_INTERVAL_MS

    print("ESP32 System Started... Total DB Records stored:", db.count())

    while True:
        try:
            mqtt.check_msg()

            if time.ticks_diff(time.ticks_ms(), last_publish) >= PUBLISH_INTERVAL_MS:
                data = sensors.read_all()
                data['timestamp'] = time.time()
                
                db.insert(data)
                
                health_score = calculate_health_score(data)

                payload = json.dumps(data)
                mqtt.publish(TOPICS["telemetry"], payload)
                mqtt.publish(TOPICS["health"], str(health_score))

                print(f"[DB Stored: {db.count()}] Telemetry Published ->", payload)

                last_publish = time.ticks_ms()

            time.sleep_ms(100)

        except Exception as e:
            print("Main loop error:", e)
            time.sleep(2)

if __name__ == "__main__":
    main()