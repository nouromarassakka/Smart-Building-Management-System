import dht
from machine import Pin, ADC

class Sensors:
    def __init__(self, dht_pin=15, ldr_pin=34, pir_pin=13, smoke_pin=35):
        self.dht = dht.DHT22(Pin(dht_pin))

        self.ldr = ADC(Pin(ldr_pin))
        try:
            self.ldr.atten(ADC.ATTN_11DB)
        except Exception:
            pass

        self.pir = Pin(pir_pin, Pin.IN)

        self.smoke = ADC(Pin(smoke_pin))
        try:
            self.smoke.atten(ADC.ATTN_11DB)
        except Exception:
            pass

    def read_all(self):
        temperature = None
        humidity = None
        try:
            self.dht.measure()
            temperature = self.dht.temperature()
            humidity = self.dht.humidity()
        except Exception as e:
            print('DHT read error:', e)

        try:
            ldr_raw = self.ldr.read()
            light = int((4095 - ldr_raw) / 4095 * 100)
        except Exception:
            light = None

        try:
            motion = int(self.pir.value())
        except Exception:
            motion = None

        try:
            smoke_raw = self.smoke.read()
            smoke = 1 if smoke_raw > 2000 else 0
        except Exception:
            smoke = None

        return {
            'temperature': temperature,
            'humidity': humidity,
            'light': light,
            'motion': motion,
            'smoke': smoke
        }