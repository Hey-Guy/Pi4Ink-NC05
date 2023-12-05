import os.path
import sys
from tkinter import *
from tkinter import messagebox
import numpy as np

import basics

if '/usr/bin' in sys.executable:  # Auswhal, ob python am Pi oder am LapTop
    import a_Extern as ziel

    print('Ziel = a_Extern')

else:
    import a_Intern as ziel

    print('Ziel = a_Intern')


def systemTest():
    fehler = False
    try:  # test ob allVorgaben.ini erreichbar
        test = int(basics.iniLesen('allVorgaben.ini', 'test lesen'))
        if test != 123456789:
            messagebox.showerror('Error Setup', 'Wert von VL99 in Ini-Datei allVorgaben.ini nicht lesbar')
            fehler = True
    except:
        messagebox.showerror('Error Setup', 'Wert von VL99 in Ini-Datei allVorgaben.ini nicht lesbar')
        fehler = True
    try:  # Test der Füllstandsensoren
        test = ziel.fuellstandGradient('VL')
        test = ziel.fuellstandGradient('RL')
    except:
        messagebox.showerror('Error Setup', 'Fühlstandssensor nicht lesbar')
        fehler = True
    return fehler


def koeffizentenTest(koeffizenten, tankName):
    hoeheWert = int(basics.iniLesen('allVorgaben.ini', 'sensor' + tankName))
    # print('koeffizenten ',koeffizenten,'\tTank ', tankName,'\thoehenWert',hoeheWert)
    wert = koeffizenten[0] * hoeheWert * hoeheWert + koeffizenten[1] * hoeheWert + koeffizenten[2]
    # print('koeffizenten ', koeffizenten, 'Tank ', tankName, '\tFüllhöhe ', hoeheWert, '\tWert ', wert, '\t')
    return


def berechneParabel(voll, halb, leer):
    matr = np.array([[voll * voll, voll, 1],
                     [halb * halb, halb, 1],
                     [leer * leer, leer, 1]])
    fullstandProzent = np.array([100, 50, 0])

    koeffizenten = np.linalg.solve(matr, fullstandProzent)

    return koeffizenten


def start(root):
    a = sys.path
    if '/usr/bin' in sys.executable:
        os.chdir(sys.path[0])
    # print('Aktuelles Verzeichnis', os.listdir())

    # ------------------------------------------------------------------Grundfenster-----------------------------------
    scaleEinFarbe = 'Black'
    farbeBack = '#181F31'
    farbeFront = "#CdCCCC"
    farbeText = '#000000'
    farbeWerte = '#FFFFFF'
    farbeTanks = 'Darkgrey'
    farbeVL = 'Darkgrey'
    farbeRL = 'Darkgrey'
    schrift1 = ('Arial', 25, 'bold italic')
    schrift2 = ('Arial', 18, 'bold italic')
    schrift3 = ('Arial', 18, 'italic')
    schriftWerte = ('Arial', 25, 'italic')
    schriftOff = 10
    # Messen der Füllstände - Definition der Variable
    fuellstandVL = ''
    fuellstandRL = ''

    # ----------------------------------------------------------------Start Grundfenster

    rootKlein = Toplevel(root)
    rootKlein.title('Farbsystem HM')
    rootKlein.geometry('460x695+5+5')  # y Ecke 400 ersetzt 1550
    fenster = Canvas(rootKlein, bd=0, width=1480, height=880, bg=farbeBack)

    bildKreuz = PhotoImage(file='KreuzKlein.png')
    bildOk = PhotoImage(file='Ok.png')

    # Hintergrundfelder
    fenster.create_rectangle(20, 20, 440, 675, fill=farbeFront)

    fenster.create_text(20 + schriftOff, 40, text='Füllsensoren einlesen', fill=farbeText, font=schrift1, anchor='w')
    fenster.pack()

    def definiereFuellstandDict():
        fuellstandDict = {'VL99': basics.iniLesen('allVorgaben.ini', 'VL99'),
                          'VL50': basics.iniLesen('allVorgaben.ini', 'VL50'),
                          'VL40': basics.iniLesen('allVorgaben.ini', 'VL40'),
                          'VL30': basics.iniLesen('allVorgaben.ini', 'VL30'),
                          'VL20': basics.iniLesen('allVorgaben.ini', 'VL20'),
                          'VL10': basics.iniLesen('allVorgaben.ini', 'VL10'),
                          'VL0': basics.iniLesen('allVorgaben.ini', 'VL0'),
                          'RL99': basics.iniLesen('allVorgaben.ini', 'RL99'),
                          'RL50': basics.iniLesen('allVorgaben.ini', 'RL50'),
                          'RL40': basics.iniLesen('allVorgaben.ini', 'RL40'),
                          'RL30': basics.iniLesen('allVorgaben.ini', 'RL30'),
                          'RL20': basics.iniLesen('allVorgaben.ini', 'RL20'),
                          'RL10': basics.iniLesen('allVorgaben.ini', 'RL10'),
                          'RL0': basics.iniLesen('allVorgaben.ini', 'RL0'),
                          'VList': basics.iniLesen('allVorgaben.ini', 'VList'),
                          'RList': basics.iniLesen('allVorgaben.ini', 'RList')}
        return fuellstandDict

    def fuellStandmessung(tankHoehe):
        global fuellstandVL, fuellstandRL
        fuellstandDict = definiereFuellstandDict()
        if 'VL' in tankHoehe:
            tank = 'VL'
            fuellstandWert = fuellstandVL
        else:
            tank = 'RL'
            fuellstandWert = fuellstandRL

        basics.iniSchreiben('allVorgaben.ini', tankHoehe, fuellstandWert)
        fuellstandDict[tankHoehe] = fuellstandWert
        print('a_setup-fuellStandmessung tankhoehe', tankHoehe, '\tfuellstandWert', fuellstandWert)

        schalterDict[tankHoehe].configure(image=bildOk)

        fenster.itemconfigure(wertFeldVL99, text=fuellstandDict['VL99'])
        fenster.itemconfigure(wertFeldVL50, text=fuellstandDict['VL50'])
        fenster.itemconfigure(wertFeldVL40, text=fuellstandDict['VL40'])
        fenster.itemconfigure(wertFeldVL30, text=fuellstandDict['VL30'])
        fenster.itemconfigure(wertFeldVL20, text=fuellstandDict['VL20'])
        fenster.itemconfigure(wertFeldVL10, text=fuellstandDict['VL10'])
        fenster.itemconfigure(wertFeldVL0, text=fuellstandDict['VL0'])
        fenster.itemconfigure(wertFeldRL99, text=fuellstandDict['RL99'])
        fenster.itemconfigure(wertFeldRL50, text=fuellstandDict['RL50'])
        fenster.itemconfigure(wertFeldRL40, text=fuellstandDict['RL40'])
        fenster.itemconfigure(wertFeldRL30, text=fuellstandDict['RL30'])
        fenster.itemconfigure(wertFeldRL20, text=fuellstandDict['RL20'])
        fenster.itemconfigure(wertFeldRL10, text=fuellstandDict['RL10'])
        fenster.itemconfigure(wertFeldRL0, text=fuellstandDict['RL0'])

    def werteFeld(x, y, wert, einheit):
        fenster.create_rectangle(x, y, x + 125, y + 50, fill=farbeWerte)
        fenster.create_text(x + 135, y + 25, text=einheit, fill=farbeText, font=schrift2, anchor='w')
        werteFeldInhalt = fenster.create_text(x + 110, y + 25, text=wert, fill=farbeText, font=schriftWerte,
                                              anchor='e')
        return werteFeldInhalt

    def schalter(x, y, text):
        schalterFeld = Button(fenster, command=lambda: fuellStandmessung(text), image=bildKreuz, compound=TOP)
        schalterFeld.configure(width=40, height=40, state=ACTIVE, anchor='c')
        schalter_window = fenster.create_window(x, y, window=schalterFeld, anchor='w')
        return schalterFeld

    def hauptschleife():
        global fuellstandVL, fuellstandRL
        fuellstandVL = str(ziel.fuellstandGradient('VL'))
        fenster.itemconfigure(wertFeldVList, text=fuellstandVL)
        fuellstandRL = str(ziel.fuellstandGradient('RL'))
        fenster.itemconfigure(wertFeldRList, text=fuellstandRL)
        fenster.after(1000, hauptschleife)

    # Wertefelder
    fuellstandDict = definiereFuellstandDict()
    wertFeldVL99 = werteFeld(80, 75, fuellstandDict['VL99'], '99')
    wertFeldVL50 = werteFeld(90, 150, fuellstandDict['VL50'], '50')
    wertFeldVL40 = werteFeld(90, 225, fuellstandDict['VL40'], '40')
    wertFeldVL30 = werteFeld(90, 300, fuellstandDict['VL30'], '30')
    wertFeldVL20 = werteFeld(90, 375, fuellstandDict['VL20'], '20')
    wertFeldVL10 = werteFeld(90, 450, fuellstandDict['VL10'], '10')
    wertFeldVL0 = werteFeld(90, 525, fuellstandDict['VL0'], '0')
    wertFeldVList = werteFeld(90, 600, fuellstandDict['VList'], 'Ist')
    wertFeldRL99 = werteFeld(255, 75, fuellstandDict['RL99'], '')
    wertFeldRL50 = werteFeld(255, 150, fuellstandDict['RL50'], '')
    wertFeldRL40 = werteFeld(255, 225, fuellstandDict['RL40'], '')
    wertFeldRL30 = werteFeld(255, 300, fuellstandDict['RL30'], '')
    wertFeldRL20 = werteFeld(255, 375, fuellstandDict['RL20'], '')
    wertFeldRL10 = werteFeld(255, 450, fuellstandDict['RL10'], '')
    wertFeldRL0 = werteFeld(255, 525, fuellstandDict['RL0'], '')
    wertFeldRList = werteFeld(255, 600, fuellstandDict['RList'], '')

    schalterDict = {'VL99': schalter(30, 100, 'VL99'),  # Positionierung der Schalter
                    'VL50': schalter(30, 175, 'VL50'),
                    'VL40': schalter(30, 250, 'VL40'),
                    'VL30': schalter(30, 325, 'VL30'),
                    'VL20': schalter(30, 400, 'VL20'),
                    'VL10': schalter(30, 475, 'VL10'),
                    'VL0': schalter(30, 550, 'VL0'),
                    'RL99': schalter(385, 100, 'RL99'),
                    'RL50': schalter(385, 175, 'RL50'),
                    'RL40': schalter(385, 250, 'RL40'),
                    'RL30': schalter(385, 325, 'RL30'),
                    'RL20': schalter(385, 400, 'RL20'),
                    'RL10': schalter(385, 475, 'RL10'),
                    'RL0': schalter(385, 550, 'RL0')
                    }

    fenster.after(1000, hauptschleife)
    rootKlein.mainloop()
