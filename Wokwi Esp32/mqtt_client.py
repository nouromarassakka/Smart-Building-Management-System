import time
from umqtt.simple import MQTTClient

class MQTTClientWrapper:
    def __init__(self, client_id, broker, port=1883, keepalive=60):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.keepalive = keepalive
        self._client = MQTTClient(client_id, broker, port=port, keepalive=keepalive)

    def set_callback(self, callback):
        self._client.set_callback(callback)

    def connect(self):
        tries = 0
        while tries < 5:
            try:
                self._client.connect()
                print('MQTT: Connected successfully to', self.broker)
                return True
            except Exception as e:
                tries += 1
                print(f'MQTT connection attempt {tries} failed:', e)
                time.sleep(2)
        return False

    def subscribe(self, topic):
        try:
            self._client.subscribe(topic)
            print('Subscribed to topic:', topic)
        except Exception as e:
            print('Subscribe error:', e)

    def publish(self, topic, msg):
        try:
            self._client.publish(topic, msg)
            return True
        except Exception as e:
            print('Publish error:', e)
            return False

    def check_msg(self):
        try:
            self._client.check_msg()
        except Exception:
            pass

    def disconnect(self):
        try:
            self._client.disconnect()
        except Exception:
            pass