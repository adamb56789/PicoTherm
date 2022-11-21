# PicoTherm
For Raspberry Pi Pico W.

Reads from a DHT22 and publishes data to an encrypted MQTT topic - tested with AWS IoT Core.

## Running the code
Create `config.py`containing:
```python
DEVICE_NAME = "your_device_name_for_mqtt_topic"
DHT22_PIN = 0 # the GPIO pin your DHT22 is connected to
READ_INTERVAL = 5*60*1000 # in milliseconds
WIFI_SSID = 'your_wifi_name'
WIFI_PASSWORD = '############'
MQTT_CLIENT_KEY = "creds/################################################################-private.pem.key"
MQTT_CLIENT_CERT = "creds/################################################################-certificate.pem.crt"
MQTT_BROKER = "##############-ats.iot.your-region.amazonaws.com"
MQTT_BROKER_CA = "creds/AmazonRootCA1.pem"
```
Create a directory named `certs` containing the files listed in `config.py`
