import time

import requests

import basics


def encode(wert):
    hexdic = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
              'D': 13, 'E': 14, 'F': 15}
    msg = 16 * hexdic[wert[0]] + hexdic[wert[1]]
    lsg = 16 * hexdic[wert[2]] + hexdic[wert[3]]
    ergebnis = 16 * 16 * msg + lsg
    return ergebnis


def fuellstand():  # Steuerung der Pumpe in Prozent
    al1120 = '192.168.1.250'
    tree = '//gettree'
    port1 = '/iolinkmaster/port[1]/iolinkdevice/pdin/getdata'
    port2 = '/iolinkmaster/port[2]/iolinkdevice/pdin/getdata'
    sensorSpritzeVoll = int(basics.iniLesen('allVorgaben.ini', 'sensorSpritzeVoll'))
    sensorSpritzeLeer = int(basics.iniLesen('allVorgaben.ini', 'sensorSpritzeLeer'))

    statusPumpe = basics.iniLesen('allSoll.ini', 'statusPumpe')
    regelfaktor = int(basics.iniLesen('allVorgaben.ini', 'regelfaktor'))

    zeitAlt = time.time()
    sollPumpe = 0
    while True:

        fuellVLwert = requests.get('http://' + al1120 + port2).json()
        fuellVLstr = fuellVLwert['data']['value']
        fuellVL = encode(fuellVLstr)
        fuellRLwert = requests.get('http://' + al1120 + port1).json()
        fuellRLstr = fuellRLwert['data']['value']
        fuellRL = encode(fuellRLstr)
        # print(fuellVL['data']['value'])

        istFuellstandVL = round((fuellVL - sensorSpritzeLeer) / (sensorSpritzeVoll - sensorSpritzeLeer), 1) * 100
        istFuellstandRL = round((fuellRL - sensorSpritzeLeer) / (sensorSpritzeVoll - sensorSpritzeLeer), 1) * 100
        if statusPumpe:
            sollPumpe += (istFuellstandRL - istFuellstandVL) * regelfaktor
        else:
            sollPumpe = 0
        if sollPumpe >= 100:
            sollPumpe = 100
        if sollPumpe < 0:
            sollPumpe = 0
        # print('FüllstandVL = ' + str(istFuellstandVL) + ' FüllstandRL = ' + str(istFuellstandRL) + ' Pumpe = ' + str(sollPumpe))
        istPumpe = sollPumpe
        zeitNeu = time.time()
        warten = zeitNeu - zeitAlt
        if warten > 3:
            statusPumpe = basics.iniLesen('allSoll.ini', 'statusPumpe')
            schreiben = basics.iniSchreiben('allSoll.ini', 'sollPumpe', sollPumpe)
            schreiben = basics.iniSchreiben('all_Ist.ini', 'istPumpe', istPumpe)
            zeitAlt =time.time()


fuellstand()
