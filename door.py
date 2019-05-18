from gpiozero import Button, LED
import time


set_relay = LED(4)


def set_on():
    set_relay.on()


def set_off():
    set_relay.off()


def doorOpen():
    set_on()
    time.sleep(1)
    set_off()
