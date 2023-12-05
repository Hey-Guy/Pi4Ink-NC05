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
    scaleFarbe = 'Red'
    schrift1 = ('Arial', 25, 'bold italic')
    schrift2 = ('Arial', 18, 'bold italic')
    schrift3 = ('Arial', 18, 'italic')
    schriftWerte = ('Arial', 25, 'italic')
    schriftOff = 10
    # Messen der Füllstände - Definition der Variable
    fuellstandVL = ''
    fuellstandRL = ''

    rootKlein = Toplevel(root)
    rootKlein.title('Farbsystem HM')
    rootKlein.geometry('460x695+600+5')  # y Ecke 400 ersetzt 1550
    fenster = Canvas(rootKlein, bd=0, width=1480, height=880, bg=farbeBack)

    bildKreuz = PhotoImage(file='../KreuzKlein.png')
    bildOk = PhotoImage(file='../Ok.png')

    # Hintergrundfelder
    fenster.create_rectangle(20, 20, 440, 675, fill=farbeFront)
    fenster.create_text(20 + schriftOff, 40, text='Ventile Schalten', fill=farbeText, font=schrift1, anchor='w')
    fenster.pack()

    GIPOs = {'ventilVL': 6,  # pin29 - Flüssigkeit
             'ventilRL': 13,  # pin31 - Flüssigkeit
             'pumpeInk': 16,  # pin33
             'Licht': 5,  # pin36
             'druckPurgen': 19,  # pin35
             'vorVentile': 20,  # pin38 - 2 mal für Vakuum und 1 für Druck
             'purgenVL': 26,  # pin40 Umschaltventil zwischen Vakuum und Purgedruck
             'purgenRL': 21}  # pin37 Umschaltventil zwischen Vakuum und Purgedruck

    #-----------------------Schalterbeschriftung einfügen
    index = 0
    for i in GIPOs:
        y = 100 + (index * 75)
        fenster.create_text(50, y, text=i, fill=farbeText, font=schriftWerte, anchor=W)
        index+=1


    def scaleEinCommand():

        return


    def schalten(wert,nameSchalter):
        print(wert, nameSchalter)
        return

    def schalter(x, y, wert,nameSchalter ):
        if wert:
            scaleFarbe = "Red"
        else:
            scaleFarbe = "Green"
        schalterFeld = Scale(fenster, command= schalten(nameSchalter), bg="Grey", orient=HORIZONTAL, width=50, sliderlength=50)
        schalterFeld.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1,  troughcolor=scaleFarbe, showvalue=False)
        fenster.create_window(x, y, anchor=CENTER, window=schalterFeld )
        return schalterFeld


    def hauptschleife():
        fenster.after(1000, hauptschleife)

    schalterDic = {'ventilVL': schalter (300,100, False, 'ventilVL')}  # pin29 - Flüssigkeit
    '''
    'ventilRL': 13,  # pin31 - Flüssigkeit
     'pumpeInk': 16,  # pin33
     'Licht': 5,  # pin36
     'druckPurgen': 19,  # pin35
     'vorVentile': 20,  # pin38 - 2 mal für Vakuum und 1 für Druck
     'purgenVL': 26,  # pin40 Umschaltventil zwischen Vakuum und Purgedruck
     'purgenRL': 21}  # pin37 Umschaltventil zwischen Vakuum und Purgedruck'''

    fenster.after(1000, hauptschleife)
    rootKlein.mainloop()

root = Tk()
start(root)