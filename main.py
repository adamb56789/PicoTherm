from machine import Pin, unique_id, Timer
from time import sleep, sleep_ms
from dht import DHT22
from umqtt.simple import MQTTClient
import network, ssl, ubinascii, ntptime

from config import DEVICE_ID, DHT22_PIN, READ_INTERVAL, WIFI_SSID, WIFI_PASSWORD, MQTT_CLIENT_KEY, MQTT_CLIENT_CERT, MQTT_BROKER, MQTT_BROKER_CA

# Wi-Fi tries to connect every second this many times
WIFI_TIMEOUT = 30

# If connection fails with an error wait this many seconds before trying again
WIFI_FAILURE_DELAY = 5

# Get a unique ID for MQTT
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())

MQTT_TOPIC = "picotherm/" + str(DEVICE_ID)

# Blink LED for signalling or debugging
def blink():
    led = Pin("LED", Pin.OUT)
    led.on()
    sleep_ms(10)
    led.off()
    sleep_ms(200)

# Reads PEM file and returns byte array of data
def read_pem(file):
    with open(file, "r") as input:
        text = input.read().strip()
        split_text = text.split("\n")
        base64_text = "".join(split_text[1:-1])
        return ubinascii.a2b_base64(base64_text)

def read(timer):
    # Connect to Wi-Fi
    print(f"Connecting to Wi-Fi SSID: {WIFI_SSID}...")
    blink()

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    tries = 0
    while tries < WIFI_TIMEOUT:
        if wlan.status() >= 3:
            blink();blink();blink()
            break
        tries += 1
        print('waiting for connection...')
        if wlan.status() == 1:
            blink()
        if wlan.status() < 0:
            # Sometimes gets errors but works when retrying, so try again
            blink();blink()
            sleep(WIFI_FAILURE_DELAY)
            wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        sleep(1)

    # Handle connection error
    status = wlan.status()
    if status != 3:
        # If connection still not working, go to sleep and try again next time
        print("Connection completely failed, giving up")
        mqtt_client.disconnect()
        wlan.disconnect()
        wlan.active(False)
        sleep(1)
    else:
        print(f"Connected to Wi-Fi SSID: {WIFI_SSID}")

    # Time may need to be accurate for TLS to work
    ntptime.settime()

    # Read credentials and certificates then connect
    key = read_pem(MQTT_CLIENT_KEY)
    cert = read_pem(MQTT_CLIENT_CERT)
    ca = read_pem(MQTT_BROKER_CA)

    mqtt_client = MQTTClient(
        MQTT_CLIENT_ID,
        MQTT_BROKER,
        keepalive=60,
        ssl=True,
        ssl_params={
            "key": key,
            "cert": cert,
            "server_hostname": MQTT_BROKER,
            "cert_reqs": ssl.CERT_REQUIRED,
            "cadata": ca,
        },
    )

    print("Connecting to broker...")
    mqtt_client.connect()
    blink()
    print("Connected to broker")

    # Read sensor on pin in config
    dht = DHT22(Pin(DHT22_PIN))

    dht.measure()
    temperature = dht.temperature()
    humidity = dht.humidity()

    print('Temperature:', temperature, 'C    Humidity:', humidity, '%')
    for i in range(temperature - 15.99):
        blink()

    # Upload the data
    json = "{" + f'"temperature":{str(temperature)},"humidity":{str(humidity)}' + "}"
    print(f"Publishing {json} to {MQTT_TOPIC}")
    mqtt_client.publish(MQTT_TOPIC, json, retain=True)
    
    # Wait to make sure it sends the data in time
    # This is probably too long but might as well be safe
    sleep(5)
    blink()
    print("Finished publishing")
    mqtt_client.disconnect()
    wlan.disconnect()
    wlan.active(False)
    sleep(1)

# Read sensor once then repeat with a given interval
# Read sensor manually once because the timer always waits the full period first
read(None)
Timer().init(period=READ_INTERVAL, mode=Timer.PERIODIC, callback=read)

