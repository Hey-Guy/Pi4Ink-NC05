import numpy as np

import basics


def berechneParabel(voll, halb, leer):
    matr = np.array([[voll * voll, voll, 1],
                     [halb * halb, halb, 1],
                     [leer * leer, leer, 1]])
    fullstandProzent = np.array([100, 50, 0])

    koeffizenten = np.linalg.solve(matr, fullstandProzent)
    print(koeffizenten)
    return koeffizenten


def testBerechnungKoef():
    voll = int(basics.iniLesen('allVorgaben.ini', 'sensorVL100'))
    halb = int(basics.iniLesen('allVorgaben.ini', 'sensorVL50'))
    leer = int(basics.iniLesen('allVorgaben.ini', 'sensorVL0'))
    koeffizentenVL = berechneParabel(voll, halb, leer)
    basics.iniSchreiben('allVorgaben.ini', 'VL_a', koeffizentenVL[0])
    basics.iniSchreiben('allVorgaben.ini', 'VL_b', koeffizentenVL[1])
    basics.iniSchreiben('allVorgaben.ini', 'VL_c', koeffizentenVL[2])

    voll = int(basics.iniLesen('allVorgaben.ini', 'sensorRL100'))
    halb = int(basics.iniLesen('allVorgaben.ini', 'sensorRL50'))
    leer = int(basics.iniLesen('allVorgaben.ini', 'sensorRL0'))
    koeffizentenRL = berechneParabel(voll, halb, leer)
    basics.iniSchreiben('allVorgaben.ini', 'RL_a', koeffizentenRL[0])
    basics.iniSchreiben('allVorgaben.ini', 'RL_b', koeffizentenRL[1])
    basics.iniSchreiben('allVorgaben.ini', 'RL_c', koeffizentenRL[2])


def testParabel(koef):
    '''voll = float(basics.iniLesen('allVorgaben.ini', 'VL_a'))
    halb = float(basics.iniLesen('allVorgaben.ini', 'VL_b'))
    leer = float(basics.iniLesen('allVorgaben.ini', 'VL_c'))'''
    voll, halb, leer = koef
    fuellstand = int(basics.iniLesen('allVorgaben.ini', 'sensorRL0'))
    fuellVL = round(voll * fuellstand * fuellstand + halb * fuellstand + leer, 3)
    return fuellVL


def werteTabelle(koef):
    voll, halb, leer = koef
    for i in range(0,21000,500):
        #i += 5000
        print('x =\t',i,'\ty = \t',round(voll * i * i + halb * i + leer, 3))


koef = berechneParabel(20000, 6000, 0)
print(werteTabelle(koef))

# testBerechnungKoef()
