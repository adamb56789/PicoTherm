from machine import Pin, Timer
from time import sleep, sleep_ms
import dht, time

led = Pin("LED", Pin.OUT)
def blink(duration):
    led.on()
    sleep_ms(10)
    led.off()
    sleep_ms(200)

dht = dht.DHT22(Pin(0))

dht.measure()
temperature = dht.temperature()
humidity = dht.humidity()
print('Temperature:', temperature, 'C    Humidity:', humidity, '%')
for i in range(temperature - 15.99):
    blink(100)
sleep(2)
