import os.path
import sys
from tkinter import *
from tkinter import messagebox
import numpy as np
import a_Interface
import basics

'''if '/usr/bin' in sys.executable:  # Auswhal, ob python am Pi oder am LapTop
    import a_Extern as ziel

    print('Ziel = a_Extern')

else:
    import a_Intern as ziel

    print('Ziel = a_Intern')'''

def start(root):

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

    GPIOs = {'ventilVL': 6,  # pin29 - Flüssigkeit
             'ventilRL': 13,  # pin31 - Flüssigkeit
             'pumpeInk': 16,  # pin33
             'Licht': 5,  # pin36
             'druckPurgen': 19,  # pin35
             'vorVentile': 20,  # pin38 - 2 mal für Vakuumvorventile  und 1 für Druckvorventil
             'purgenVL': 26,  # pin40 Umschaltventil zwischen Vakuum und Purgedruck
             'purgenRL': 21}  # pin37 Umschaltventil zwischen Vakuum und Purgedruck

    rootKlein = Toplevel(root)
    rootKlein.title('Farbsystem HM')
    rootKlein.geometry('460x900+1400+50')  # y Ecke 400 ersetzt 1550
    fenster = Canvas(rootKlein, bd=0, width=460, height=900, bg=farbeBack)

    bildKreuz = PhotoImage(file='KreuzKlein.png')
    bildOk = PhotoImage(file='Ok.png')
    bildPumpeAuf = PhotoImage(file='Pumpe-auf.png')
    bildPumpeZu = PhotoImage(file='Pumpe-zu.png')
    bildVakuumPumpe = bildPumpeZu
    bildVentilAuf = PhotoImage(file='Ventil-auf.png')
    bildVentilZu = PhotoImage(file='Ventil-zu.png')
    bildVorventile = bildVentilZu
    bildPurgLuftVL = PhotoImage(file='Ventillinks.png')
    bildPurgLuftRL = PhotoImage(file='Ventilrechts.png')
    bildPurgVL = bildVentilAuf
    bildPurgRL = bildVentilAuf
    status = a_Interface.relaisStatus(GPIOs['purgenVL'])
    if status:
        bildPurgRL = bildVentilAuf
    else:
        bildPurgRL = bildPurgLuftRL

    status = a_Interface.relaisStatus(GPIOs['purgenRL'])
    if status:
        bildPurgVL = bildVentilAuf
    else:
        bildPurgVL = bildPurgLuftVL

    status = a_Interface.relaisStatus(GPIOs['vorVentile'])
    if status:
        bildVorventile = bildVentilZu
    else:
        bildVorventile = bildVentilAuf

    # Hintergrundfelder

    fenster.create_rectangle(20, 20, 440, 880, fill=farbeFront)
    fenster.create_text(220, 40, text='Vakuum/Luft', fill=farbeText, font=schrift1, anchor=CENTER)
    fenster.create_text(220, 80, text='Vorlauf             Rücklauf', fill=farbeText, font=schrift2, anchor=CENTER)
    #Leitungen
    xVL = 110
    xRL = 330
    mitte = 220
    quer1 = 300
    quer2 = 550
    unten = 830
    fenster.create_rectangle(mitte - 5, 100, mitte + 5, quer1, fill='Darkgrey', outline='Darkgrey')
    fenster.create_rectangle(xVL-5 , quer1, xVL+5 , unten, fill='Darkgrey', outline='Darkgrey')
    fenster.create_rectangle(xRL - 5, quer1, xRL + 5, unten, fill='Darkgrey', outline='Darkgrey')
    fenster.create_rectangle(xVL-5, quer1 -5, xRL+5, quer1+5, fill='Darkgrey', outline='Darkgrey')
    fenster.create_rectangle(xVL - 5, quer2 - 5, xRL + 5, quer2 + 5, fill='Darkgrey', outline='Darkgrey')
    fenster.create_rectangle(mitte - 5, quer2, mitte + 5, unten, fill='Darkgrey', outline='Darkgrey')
    fenster.pack()


    #--------------------------Status Variablen setzen

    # Druckregler: Bei Druck wird auf Maximaldruck von Intensiv geregelt
    #fenster.create_rectangle( mitte - 50 , quer2 - 20,  mitte + 50, quer2 + 20, fill=farbeWerte)
    #labelLuft = fenster.create_text(mitte, quer2, text="Wert", fill=farbeText, font=schriftWerte,   anchor=CENTER)

    def buttonLuft(wert):  # spülen Luft
        wert = scaleLuft.get()
        if wert == 1:
            luftDruck = float(basics.iniLesen('allVorgaben.ini',"staerke intensiv"))
            scaleLuftFarbe="Green"
        else:
            luftDruck = 0
            scaleLuftFarbe = "Darkred"
        a_Interface.regler('reglerPurgen', luftDruck)
        buttonVentilLuft.configure(troughcolor = scaleLuftFarbe)
        print(wert, luftDruck)
        return
    scaleLuft = DoubleVar()
    scaleLuft.set(0)
    buttonVentilLuft = Scale(fenster, variable = scaleLuft, bg="Grey",command=buttonLuft, font=schrift2)
    buttonVentilLuft.configure(activebackground="Grey", relief=FLAT,command=buttonLuft, troughcolor ='Darkred')
    buttonVentilLuft.configure(from_=1, to=0 ,width=50, length= 80,sliderlength=25,showvalue=0)
    buttonLuft_window = fenster.create_window(mitte, quer2, anchor=CENTER, window=buttonVentilLuft)
    
    def buttonVorventile():
        statusVorventile = a_Interface.relaisStatus(GPIOs['vorVentile'])
        statusVorventile != (statusVorventile)
        if statusVorventile :
            a_Interface.schalter('vorVentile', True)
            bildVentil = bildVentilAuf
        else:
            a_Interface.schalter('vorVentile', False)
            bildVentil = bildVentilZu
        buttonVentVakVL.configure(image=bildVentil)
        buttonVentVakRL.configure(image=bildVentil)
        buttonVentLuft.configure(image=bildVentil)
        print(statusVorventile)
        return

    buttonVentVakVL = Button(fenster, command=buttonVorventile, image=bildVorventile, compound=TOP)
    buttonVentVakVL.configure(width=80, height=80, state=ACTIVE, anchor=CENTER)
    buttonVakuumVL_window = fenster.create_window(xVL, quer1+100, window=buttonVentVakVL)

    buttonVentVakRL = Button(fenster, command=buttonVorventile, image=bildVorventile, compound=TOP)
    buttonVentVakRL.configure(width=80, height=80, state=ACTIVE, anchor=CENTER)
    buttonVakuumRL_window = fenster.create_window(xRL, quer1+100, window=buttonVentVakRL)

    buttonVentLuft = Button(fenster, command=buttonVorventile, image=bildVorventile, compound=TOP)
    buttonVentLuft.configure(width=80, height=80, state=ACTIVE, anchor=CENTER)
    buttonVakuumRL_window = fenster.create_window(mitte, quer2 + 200, window=buttonVentLuft)

    def buttonPurgVL():
        statusPurgVL = a_Interface.relaisStatus(GPIOs['purgenVL'])
        statusPurgVL != (statusPurgVL)
        if statusPurgVL :
            a_Interface.schalter('purgenVL', True)
            bildVentil = bildPurgLuftVL
        else:
            a_Interface.schalter('purgenVL', False)
            bildVentil = bildVentilAuf
        buttonVentPurgVL.configure(image=bildVentil)
        print(statusPurgVL)
        return

    buttonVentPurgVL = Button(fenster, command=buttonPurgVL, image=bildPurgVL, compound=TOP)
    buttonVentPurgVL.configure(width=80, height=80, state=ACTIVE, anchor=CENTER)
    buttonPurguumVL_window = fenster.create_window(xVL, quer2, window=buttonVentPurgVL)

    def buttonPurgRL():
        statusPurgRL = a_Interface.relaisStatus(GPIOs['purgenRL'])
        statusPurgRL != (statusPurgRL)
        if statusPurgRL :
            a_Interface.schalter('purgenRL', True)
            bildVentil = bildPurgLuftRL
        else:
            a_Interface.schalter('purgenRL', False)
            bildVentil = bildVentilAuf
        buttonVentPurgRL.configure(image=bildVentil)
        print(statusPurgRL)
        return

    buttonVentPurgRL = Button(fenster, command=buttonPurgRL, image=bildPurgRL, compound=TOP)
    buttonVentPurgRL.configure(width=80, height=80, state=ACTIVE, anchor=CENTER)
    buttonPurguumRL_window = fenster.create_window(xRL, quer2, window=buttonVentPurgRL)

    buttonVentilPumpe = Button(fenster,  image=bildVakuumPumpe, compound=TOP)
    buttonVentilPumpe.configure(width=80, height=80, state=DISABLED, anchor=CENTER)
    buttonPumpe_window = fenster.create_window(mitte, 200, window=buttonVentilPumpe)

    def hauptschleife():
        fenster.after(1000, hauptschleife)

    fenster.after(1000, hauptschleife)
    rootKlein.mainloop()

'''root = Tk()
start(root)'''