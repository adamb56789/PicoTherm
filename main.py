from machine import Pin, Timer
from time import sleep, sleep_ms
import dht, time

led = Pin("LED", Pin.OUT)
def blink(duration):
    led.on()
    sleep_ms(duration)
    led.off()
    sleep_ms(duration)

def led_morse(message):
    DOT = 10
    MORSE_CODE_DICT = {'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.','F':'..-.', 'G':'--.', 'H':'....','I':'..', 'J':'.---', 'K':'-.-','L':'.-..', 'M':'--', 'N':'-.','O':'---', 'P':'.--.', 'Q':'--.-','R':'.-.', 'S':'...', 'T':'-','U':'..-', 'V':'...-', 'W':'.--','X':'-..-', 'Y':'-.--', 'Z':'--..','1':'.----', '2':'..---', '3':'...--','4':'....-', '5':'.....', '6':'-....','7':'--...', '8':'---..', '9':'----.','0':'-----', ', ':'--..--', '.':'.-.-.-','?':'..--..', '/':'-..-.', '-':'-....-','(':'-.--.', ')':'-.--.-'}
    morse = ''
    for letter in message.upper():
        if letter != ' ':
            morse += MORSE_CODE_DICT[letter] + ' '
        else:
            morse += '/ '

    
    for c in morse:
        if c == ".":
            blink(DOT)
        elif c == "-":
            blink(DOT * 3)
        elif c == " ":
            sleep_ms(DOT * 3)
        elif c == "/":
            sleep_ms(DOT)

# led_morse("Hello World")

dht = dht.DHT22(Pin(2))
while True:
    dht.measure()
    temperature = dht.temperature()
    humidity = dht.humidity()
    print('Temperature:', temperature, 'C    Humidity:', humidity, '%')
    for i in range(temperature - 15.99):
        blink(100)
    sleep(2)
