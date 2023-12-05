'''
#Ventile schalten
GIPOs = {'ventilVL': 5,  # pin29 - Flüssigkeit
         'ventilRL': 6,  # pin31 - Flüssigkeit
         'pumpeInk': 13,  # pin33
         'pumpeVakuum': 16,  # pin36
         'druckPurgen': 19,  # pin35
         'vorVentile': 20,  # pin38 - 2 mal für Vakuum und 1 für Druck
         'purgenVL': 21,  # pin40 Umschaltventil zwischen Vakuum und Purgedruck
         'purgenRL': 26}  # pin37 Umschaltventil zwischen Vakuum und Purgedruck

a_Interface.setup(4, 4)
a_Interface.start()
a_Interface.stop()
#a_Interface.schalter('vorVentile', True)
a_Interface.schalter('purgenVL', False)
'''
import basics

# Füsstandsensoren auslesen


def fuellstandssensoren():  # Messung von Sensorwert
    from tkinter import messagebox
    import sys
    import requests
    def encode(wert):
        hexdic = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11,
                  'C': 12,
                  'D': 13, 'E': 14, 'F': 15}
        msg = 16 * hexdic[wert[0]] + hexdic[wert[1]]
        lsg = 16 * hexdic[wert[2]] + hexdic[wert[3]]
        ergebnis = 16 * 16 * msg + lsg
        return ergebnis

    def fuellstandSensor(port):

        al1120 = '192.168.1.250'
        fuellwert = -1
        try:
            fuellwert = requests.get('http://' + al1120 + port).json()
        except:
            titel = 'Fehler in a_Extern'
            meldung = 'Keine Verbindung zu Füllstandsensoren - Abbrechen'
            antwort = messagebox.askokcancel(titel, meldung, default='cancel')
            if antwort == 'cancel':
                sys.exit(titel + ': ' + meldung)
        return fuellwert

    # tree = '//gettree'
    port1RL = '/iolinkmaster/port[1]/iolinkdevice/pdin/getdata'
    port2VL = '/iolinkmaster/port[2]/iolinkdevice/pdin/getdata'
    fuellVLwert = fuellstandSensor(port2VL)
    fuellVLstr = fuellVLwert['data']['value']
    fuellVL = encode(fuellVLstr)
    fuellRLwert = fuellstandSensor(port1RL)
    fuellRLstr = fuellRLwert['data']['value']
    fuellRL = encode(fuellRLstr)
    print('Sensor: fuellVL ', fuellVL, '\tfuellRL ', fuellRL)

#Füllstandsensoren
'''
while True:
    import time

    fuellstandssensoren()
    time.sleep(1)
'''

#Mikroe ADAC

# Mikroe ADAC
def mikroe(channel, wert):
    import smbus2 as smbus
    import a_Interface
    def in_MSB_LSB(wert):
        msb = int(wert / 0xFF)
        lsb = int(wert - (msb * 0xFF))
        return msb, lsb

    DAC = {'reglerVL': 0b00010000,  # sollVL
           'reglerRL': 0b00010001,  # soolRL
           'reglerPumpe': 0b00010010,  # sollPumpe Flüssigkeit
           'reglerVakuum': 0b00010011,  # sollLeistung für Vakuumpupe
           'reglerPurgen': 0b00010100}  # Druck beim Purgen

    a_Interface.setup(4, 4)
    a_Interface.start()
    a_Interface.stop()
    a_Interface.schalter('vorVentile', True)
    a_Interface.schalter('purgenVL', True)
    a_Interface.schalter('purgenRL', True)

    i2cKanal = smbus.SMBus(1)
    i2cKanal.write_i2c_block_data(0x10, 0b00000101, [0b00000000, 0b00111111])  # pin 0 - 3 als DACs
    msb, lsb = in_MSB_LSB(wert)
    print(channel, '\tMSB\t', msb, ' \lsb\t', lsb)
    try:
        i2cKanal.write_i2c_block_data(0x10, DAC[channel], [msb, lsb])
    except:
        meldung = 'Schreibfehler am I2C des DAC'
        print('a_Extreme', meldung)
    i2cKanal.close()
    return


#mikroe('reglerPurgen', 000)

'''
# Test von Purgen
import  a_Interface
a_Interface.setup(4, 4)
a_Interface.start()
a_Interface.schalter('pumpeVakuum', 0)
a_Interface.purgen('spuelen', 1)
a_Interface.stop()
'''

basics.iniSchreiben('allVorgaben.ini', 'sollVL', -1)