import time

import RPi.GPIO as GPIO

import regelventile

global meniskus, differenz, istVL, istRL, istPumpe, fuellstandVL, fuellstandRL, statusVL, statusRL, statusPumpe

GIPOs = {'ventilVL': 5,  # pin29 - Flüssigkeit
         'ventilRL': 6,  # pin31 - Flüssigkeit
         'pumpeInk': 13,  # pin33
         'pumpeVakuum': 16,  # pin36
         'druckSpuelen': 19,  # pin35
         'vakuumVL': 20,  # pin38
         'vakuumRL': 21,  # pin40
         'frei': 26}  # pin37


def schalter(GIPOs, channel, wert) -> object:
    GPIO.output(GIPOs[channel], not (wert))  # False = Ein; True = Aus
    return


def setup():
    GIPOs = {'ventilVL': 5,  # pin29 - Flüssigkeit
             'ventilRL': 6,  # pin31 - Flüssigkeit
             'pumpeInk': 13,  # pin33
             'pumpeVakuum': 16,  # pin36
             'druckSpuelen': 19,  # pin35
             'vakuumVL': 20,  # pin38
             'vakuumRL': 21,  # pin40
             'frei': 26}  # pin37
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in GIPOs:
        GPIO.setup(GIPOs[pin], GPIO.OUT)
        schalter(GIPOs ,pin, True)
        time.sleep(0.1)
        schalter(GIPOs ,pin, False)
    schalter(GIPOs,'pumpeVakuum', True)  # Vakuumpumpe ein
    return


def startAuto(sollVL, sollRL):
    #setup()
    schalter(GIPOs,'vakuumVL', True)
    schalter(GIPOs,'vakuumRL', True)
    schalter(GIPOs,'pumpeInk',True)
    #regelventile.vakuumventile(1, sollVL)
    #regelventile.vakuumventile(0, sollRL)
    #regelventile.pumpeDef(0)
    schalter(GIPOs,'ventilVL', True)
    schalter(GIPOs,'ventilRL', True)
    return


def stoppAuto():
    for pin in GIPOs:
        schalter(GIPOs,pin, False)
    regelventile.vakuumventile(1, 0)
    regelventile.vakuumventile(0, 0)
    return
#setup()