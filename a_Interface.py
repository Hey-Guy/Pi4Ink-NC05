import sys
import time

import basics

if '/usr/bin' in sys.executable:  # Auswhal, ob python am Pi oder am LapTop
    import a_Extern as ziel
else:
    import a_Intern as ziel
# print('Ziel = a_Extern', )

GPIOs = {'ventilVL': 6,  # pin29 - Flüssigkeit
         'ventilRL': 13,  # pin31 - Flüssigkeit
         'pumpeInk': 16,  # pin33
         'Licht': 5,  # pin36
         'druckPurgen': 19,  # pin35
         'vorVentile': 20,  # pin38 - 2 mal für Vakuum und 1 für Druck
         'purgenVL': 26,  # pin40 Umschaltventil zwischen Vakuum und Purgedruck
         'purgenRL': 21}  # pin37 Umschaltventil zwischen Vakuum und Purgedruck

ADCs = {'vakuum': 'in2/ref',
        'pumpe': 'in0/ref'}

def relaisStatus(ausgang):
    status = ziel.relaisStatus(ausgang)
    return status

def purgen(name, sollPumpe) -> object:  # name: spuelen oder intensiv
    def rampe(zeit, startDruck, stopDruck):
        startZeit = time.time()  # in sekunden
        stufenZeit = 0.2  # TODO: Anzahl der Schaltungen pro Sekunde messen
        stufen = int(zeit / stufenZeit)
        deltaDruck = (stopDruck - startDruck) / stufen
        druck = startDruck
        stufDurchlauf = 0
        for i in range(stufen):
            deltaZeit = time.time() - startZeit
            while (deltaZeit < i * stufenZeit):
                time.sleep(0.01)
                deltaZeit = time.time() - startZeit
            druck = round(druck + deltaDruck, 3)  # round damit keine negativen Werte
            ziel.regler('reglerPurgen', druck)
            print('a_Interface purgen: Zeit ', round(deltaZeit, 3), '\tDruck ', druck)
            stufDurchlauf += 1

    vorlauf = float(basics.iniLesen('allVorgaben.ini', 'vorlauf ' + name))  # name = {normal, intensiv, maxVL, maxRL)
    dauer = float(basics.iniLesen('allVorgaben.ini', 'dauer ' + name))
    nachlauf = float(basics.iniLesen('allVorgaben.ini', 'nachlauf ' + name))
    staerke = float(basics.iniLesen('allVorgaben.ini', 'staerke ' + name))

    ziel.regler('reglerPumpe', 0)
    ziel.regler('reglerPurgen', 0)
    ziel.schalter(GPIOs, 'purgenVL', True)
    ziel.schalter(GPIOs, 'purgenRL', True)
    if 'VL' in name:
        ziel.schalter(GPIOs, 'purgenRL', False)
    if 'RL' in name:
        ziel.schalter(GPIOs, 'purgenVL', False)
    ziel.schalter(GPIOs, 'druckPurgen', True)
    rampe(vorlauf, 0, staerke)
    rampe(dauer, staerke, staerke)
    rampe(nachlauf, staerke, 0)
    ziel.regler('reglerPurgen', 0)
    ziel.schalter(GPIOs, 'purgenVL', False)
    ziel.schalter(GPIOs, 'purgenRL', False)
    ziel.regler('reglerPumpe', sollPumpe)


def fuellstandNormierungStufen(fuellsensor, tank):  # Linear zwischen 0 und 20% und 20% bis 100% -2 Geraden
    stufen = [0, 10, 20, 30, 40, 50, 99]  # 99, wegen unterschied zwischen 10 und 100
    fuellEichung = []
    for i in stufen:
        titel = tank + str(i)
        fuellEichung.append(float(basics.iniLesen('allVorgaben.ini', titel)))
    schritteLen = len(stufen) - 1
    if fuellsensor >= fuellEichung[schritteLen]:  # Messwert ist größer als Maximalwert
        m = (stufen[schritteLen] - stufen[schritteLen - 1]) / (
                fuellEichung[schritteLen] - fuellEichung[schritteLen - 1])
        t = stufen[schritteLen] - m * fuellEichung[schritteLen]
    else:
        for i in range(0, schritteLen):
            if fuellsensor < fuellEichung[i + 1]:
                if fuellEichung[i + 1] != fuellEichung[i]:  # Abfangen von gleichen Eichwerten
                    m = (stufen[i + 1] - stufen[i]) / (fuellEichung[i + 1] - fuellEichung[i])
                    t = stufen[i] - m * fuellEichung[i]
                    break
                else:
                    m = 1
                    t = fuellEichung[0]
    fuellProzent = m * fuellsensor + t
    if fuellProzent < 0:
        fuellProzent = 0
    # print('a_Interface m ', m, '\t t', t, '\tfuellProzent', fuellProzent ,'fuellEichung', fuellEichung)
    return fuellProzent


def fuellstandMessen(sollPumpe, statusPumpe, fuellVLalt, fuellRLalt):
    empfindlichkeit = 0.05
    empfindlichkeitDelta = 0.001

    deltaAlt = fuellRLalt - fuellVLalt
    N=3
    fuellVLsensor=0
    fuellRLsensor = 0
    for i in range(N):       #Mittelwert über N Messungen
        fuellVLsensor += ziel.fuellstandGradient('VL')
        fuellRLsensor += ziel.fuellstandGradient('RL')

    fuellVL = fuellstandNormierungStufen(fuellVLsensor/N, 'VL')
    fuellRL = fuellstandNormierungStufen(fuellRLsensor/N, 'RL')

    delta = fuellRL - fuellVL
    regelfaktor = delta
    if statusPumpe == 'auto':
        if abs(delta) > abs(deltaAlt):  # falls Unerschied der Füllhöhen sinkt, Pumpleistung bleibt gleich
            regelfaktor = delta
            # print('Fall 1', abs(delta) - abs(deltaAlt))
        elif abs(delta) == 0:
            regelfaktor = 0
        else:
            regelfaktor = -deltaAlt * abs(delta) * empfindlichkeitDelta
            # print('Fall 2', regelfaktor)

    '''mittelVL = (fuellVL + fuellVLalt) / 2
    mittelRL = (fuellRL + fuellRLalt) / 2
    delta = mittelRL - mittelVL

    regelfaktor = delta * abs(delta)'''

    if sollPumpe > 99:
        sollPumpe = 99
    if sollPumpe < 0:
        sollPumpe = 0

    sollPumpe += regelfaktor * empfindlichkeit
    regler('reglerPumpe', sollPumpe)

    fuellVL = round(fuellVL, 3)
    fuellRL = round(fuellRL, 3)

    # print('fuellVl: ', fuellVL, '\tfuellRl: ', fuellRL, '  delta: ', delta, deltaAlt)
    # print('SollPumpe in fuelstand:', sollPumpe, '\tStatus: ',statusPumpe)
    # print('FüllstandVL = ' + str(fuellVL) + ' FüllstandRL = ' + str(fuellRL) + ' Pumpe = ' + str(sollPumpe))
    return sollPumpe, fuellVL, fuellRL


def setup(sollVL, sollRL):
    ziel.setupRelais(GPIOs)  # alle Relais auf False
    ziel.setupRegler()
    ziel.schalter(GPIOs, 'Licht', True)
    ziel.schalter(GPIOs, 'vorVentile', True)
    ziel.regler('reglerVL', sollVL)
    ziel.regler('reglerRL', sollRL)
    startVakuum = int(basics.iniLesen('allVorgaben.ini', 'startVakuum'))
    ziel.regler('reglerVakuum', startVakuum)
    ziel.schalter(GPIOs, 'Licht', True)  # Vakuumpumpe ein
    ziel.regler('reglerPurgen', 0)


def start():
    ziel.schalter(GPIOs, 'ventilVL', True)
    ziel.schalter(GPIOs, 'ventilRL', True)
    ziel.schalter(GPIOs, 'pumpeInk', True)
    ziel.schalter(GPIOs, 'Licht', True)
    sollPumpeVakuum = int(basics.iniLesen('allVorgaben.ini', 'hochVakuum'))
    ziel.regler('reglerVakuum', sollPumpeVakuum)
    ziel.schalter(GPIOs, 'vorVentile', True)  # Vakuumpumpe ein


def stop() -> object:
    pause = 0.1
    ziel.schalter(GPIOs, 'ventilVL', False)
    time.sleep(pause)
    ziel.schalter(GPIOs, 'ventilRL', False)
    time.sleep(pause)
    ziel.regler('reglerPumpe', 0)
    ziel.schalter(GPIOs, 'pumpeInk', False)
    time.sleep(pause)
    ziel.schalter(GPIOs, 'Licht', False)
    time.sleep(pause)
    ziel.regler("reglerVakuum", 10)
    time.sleep(pause)
    ziel.regler('reglerPurgen', 0)
    ziel.schalter(GPIOs, 'druckPurgen', False)
    time.sleep(pause)
    ziel.schalter(GPIOs, 'vorVentile', False)
    time.sleep(pause)
    ziel.schalter(GPIOs, 'purgenVL', False)
    time.sleep(pause)
    ziel.schalter(GPIOs, 'purgenRL', False)
    time.sleep(pause)


def schalter(channel, wert):
    ziel.schalter(GPIOs, channel, wert)


def regler(channel, wert):
    ziel.regler(channel, wert)


def adc_mess(channel):
    # ziel.adc_mess(channel) für ADAC Mikroe-2690 -
    eingang = ziel.adc1015Wert(channel)
    return eingang
