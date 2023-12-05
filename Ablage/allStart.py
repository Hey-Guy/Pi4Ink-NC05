from random import *
from tkinter import *

import allRelais
import basics

# import regelventile

# ------------------------------------------------------------------Grundfenster-----------------------------------
scaleEinFarbe = 'Black'
farbeBack = '#181F31'
farbeFront = "#CdCCCC"
farbeText = '#000000'
farbeWerte = '#FFFFFF'
farbeTanks = 'Darkgrey'
farbeVL = 'Darkgrey'
farbeRL = 'Darkgrey'
schrift1 = ('Arial', 16, 'bold italic')
schrift2 = ('Arial', 14, 'bold italic')
schriftWerte = ('Arial', 16, 'bold italic')
schriftOff = 10
root = Tk()
root.title('Farbsystem HM')
root.geometry('1500x900+400+50')
fenster = Canvas(root, bd=0, width=1480, height=880, bg=farbeBack)
# fenster.pack()

# Setup-------------------------------------------------------------Setup------------------------------------------
global meniskus, differenz, istVL, istRL, istPumpe, fuellstandVL, fuellstandRL, statusVL, statusRL, statusPumpe

# Werte aus allVorgaben.ini und allSoll.ini einlesen
sollVL = DoubleVar()
istVL = DoubleVar()
sollRL = DoubleVar()
istRL = DoubleVar()

statusVL = basics.iniLesen('allVorgaben.ini', 'statusVL')
sollVL = round(float(basics.iniLesen('allSoll.ini', 'sollVL')), 1)
statusRL = basics.iniLesen('allVorgaben.ini', 'statusRL')
sollRL = round(float(basics.iniLesen('allSoll.ini', 'sollRL')), 1)
statusPumpe = basics.iniLesen('allVorgaben.ini', 'statusPumpe')
sollPumpe = round(float(basics.iniLesen('allSoll.ini', 'sollPumpe')), 1)
statusPumpe = basics.iniLesen('allVorgaben.ini', 'statusPumpeVak')
sollPumpe = round(float(basics.iniLesen('allVorgaben.ini', 'sollPumpeVak')), 1)
statusDruck = basics.iniLesen('allVorgaben.ini', 'statusDruck')
sollPumpe = round(float(basics.iniLesen('allVorgaben.ini', 'sollDruck')), 1)

# Ist-Werte von Füllstandsregler
istVL = round(float(basics.iniLesen('all_Ist.ini', 'istVL')), 1)
istRL = round(float(basics.iniLesen('all_Ist.ini', 'istRL')), 1)
fuellstandVL = round(float(basics.iniLesen('all_Ist.ini', 'fuellstandVL')), 1)
fuellstandRL = round(float(basics.iniLesen('all_Ist.ini', 'fuellstandRL')), 1)
istPumpe = round(float(basics.iniLesen('all_Ist.ini', 'istPumpe')), 1)

# Schalter
scaleVakuum = int(basics.iniLesen('allVorgaben.ini', 'scaleVakuum'))  # Schaltervorgaben
scaleDruckLos = basics.iniLesen('allVorgaben.ini', 'scaleDruckLos')
scaleDruckluft = basics.iniLesen('allVorgaben.ini', 'scaleDruckluft')

# Eingriffsgrenzen
fuellstandOEG = basics.iniLesen('allVorgaben.ini', 'FuellstandOEG')
fuellstandSoll = basics.iniLesen('allVorgaben.ini', 'FuellstandSoll')
fuelstandUEG = basics.iniLesen('allVorgaben.ini', 'FuellstandUEG')

# Definition der Images fuer Buttons
bildVentilAuf = PhotoImage(file='../Ventil-auf.png')
bildVentilZu = PhotoImage(file='../Ventil-zu.png')
bildVentil = bildVentilZu
bildPumpeAuf = PhotoImage(file='../Pumpe-auf.png')
bildPumpeZu = PhotoImage(file='../Pumpe-zu.png')
bildPumpe = bildPumpeZu
bildKreuz = PhotoImage(file='../Kreuz.png')


# --------------------------------------------------Hochfahren der Anlage---------------------------------------

# Schalten von Ventil und Zirkulation----------------------------------------------------------------------------
def schaltenRL(wert):
    global statusRL
    statusRL = wert
    if wert:
        bildVentil = bildVentilAuf
    else:
        bildVentil = bildVentilZu
    buttonVentilRL.configure(image=bildVentil)
    print('Ventil RL:', statusRL)


def schaltenVL(wert):
    global statusVL
    statusVL = wert
    if wert:
        bildVentil = bildVentilAuf
    else:
        bildVentil = bildVentilZu
    buttonVentilVL.configure(image=bildVentil)
    print('Ventil VL:', statusVL)


def schaltenPumpe(wert):
    global statusPumpe
    statusPumpe = wert
    if wert:
        bildPumpe = bildPumpeAuf
    else:
        bildPumpe = bildPumpeZu
    buttonVentilPumpe.configure(image=bildPumpe)
    print('Pumpe:', statusPumpe)


# Schiebeschalter
scaleFarbe = 'Red'
scaleFarbeVentil = 'Darkred'
scaleFarbeZirk = 'Darkred'
scaleFarbeSensor = 'Darkred'
buttonFarbe = 'Blue'


def scaleEinCommand(wertStr):  # Uebergabe ist String
    wert = int(wertStr)
    if wert == 1:
        scaleFarbe = 'Green'
        buttonVentilNormal.configure(state=ACTIVE)
        buttonVentilIntensiv.configure(state=ACTIVE)
        buttonEinstellungen.configure(state=ACTIVE)
        allRelais.startAuto(sollVL, sollRL)
        schaltenVL(True)
        schaltenRL(True)
        schaltenPumpe(True)

    else:
        scaleFarbe = 'Darkred'
        scaleVentil.set(0)
        scaleFarbeVentil = 'Darkred'
        buttonVentilNormal.configure(state=DISABLED)
        buttonVentilIntensiv.configure(state=DISABLED)
        scaleVentilDef.configure(troughcolor=scaleFarbeVentil)
        scaleZirk.set(0)
        scaleFarbeZirk = 'Darkred'
        scaleZirkDef.configure(troughcolor=scaleFarbeZirk)
        scaleSensor.set(0)
        scaleFarbeSensor = 'Darkred'
        scaleSensorDef.configure(troughcolor=scaleFarbeSensor)
        buttonVentilRL.configure(state=DISABLED)
        buttonVentilVL.configure(state=DISABLED)
        buttonVentilPumpe.configure(state=DISABLED)
        buttonEinstellungen.configure(state=DISABLED)
        schaltenVL(False)
        schaltenRL(False)
        schaltenPumpe(False)

        allRelais.stoppAuto()

    scale.configure(troughcolor=scaleFarbe)
    return


scaleEin = DoubleVar()
scale = Scale(fenster, variable=scaleEin, bg="Grey", orient=HORIZONTAL, width=50, sliderlength=50)
scale.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0, troughcolor=scaleFarbe,
                command=scaleEinCommand)
scale_window = fenster.create_window(200, 100, anchor=CENTER, window=scale, )


def scaleVentilCommand(wertStr):  # Uebergabe ist String

    wert = int(wertStr)
    if wert == 1 and scaleEin.get() == 1:
        farbe = 'Green'
        buttonVentilRL.configure(state=ACTIVE)
        buttonVentilVL.configure(state=ACTIVE)
        buttonVentilPumpe.configure(state=ACTIVE)
    else:
        farbe = 'Darkred'
        scaleVentil.set(0)
        buttonVentilRL.configure(state=DISABLED)
        buttonVentilVL.configure(state=DISABLED)
        buttonVentilPumpe.configure(state=DISABLED)

    scaleVentilDef.configure(troughcolor=farbe)
    return


scaleVentil = DoubleVar()
scaleVentilDef = Scale(fenster, variable=scaleVentil, bg="Grey", orient=HORIZONTAL, width=40, sliderlength=50)
scaleVentilDef.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0,
                         troughcolor=scaleFarbeVentil, command=scaleVentilCommand)
scale_window_Ventil = fenster.create_window(1065, 700, anchor=W, window=scaleVentilDef)


def scaleZirkCommand(wertStr):  # Uebergabe ist String
    wert = int(wertStr)

    if wert == 1 and scaleEin.get() == 1:
        farbe = 'Green'
        schaltenPumpe(False)


    else:
        farbe = 'Darkred'
        scaleZirk.set(0)

    scaleZirkDef.configure(troughcolor=farbe)

    return


scaleZirk = DoubleVar()
scaleZirkDef = Scale(fenster, variable=scaleZirk, bg="Grey", orient=HORIZONTAL, width=40, sliderlength=50)
scaleZirkDef.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0, troughcolor=scaleFarbeZirk,
                       command=scaleZirkCommand)
scale_window_Zirk = fenster.create_window(1065, 760, anchor=W, window=scaleZirkDef)


def scaleSensorCommand(wertStr):  # Uebergabe ist String
    wert = int(wertStr)
    if wert == 1 and scaleEin.get() == 1:
        scaleFarbe1 = 'Green'
    else:
        scaleFarbe1 = 'Darkred'
        scaleSensor.set(0)
    scaleSensorDef.configure(troughcolor=scaleFarbe1)
    return


scaleSensor = DoubleVar()
scaleSensorDef = Scale(fenster, variable=scaleSensor, bg="Grey", orient=HORIZONTAL, width=40, sliderlength=50)
scaleSensorDef.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0,
                         troughcolor=scaleFarbeSensor, command=scaleSensorCommand)
scale_window_Sensor = fenster.create_window(1065, 820, anchor=W, window=scaleSensorDef)


# Button
def buttonNormal():
    wert = scaleEin.get()
    print('Wert', wert)
    if wert == 1:
        print('Spuelen')
    return


buttonVentilNormal = Button(fenster, text="Normal", command=buttonNormal, font=schrift2, )
buttonVentilNormal.configure(width=15, height=3, fg='White', bg='Grey', relief=RAISED, state=DISABLED)
button1_window = fenster.create_window(158, 365, anchor=CENTER, window=buttonVentilNormal)


def buttonIntensiv():
    wert = scaleEin.get()
    print('Wert', wert)
    if wert == 1:
        print('Intensiv')
    return


buttonVentilIntensiv = Button(fenster, text="Intensiv", command=buttonIntensiv, font=schrift2, )
buttonVentilIntensiv.configure(width=15, height=3, fg='White', bg='Grey', relief=RAISED, state=DISABLED)
button2_window = fenster.create_window(158, 500, anchor=CENTER, window=buttonVentilIntensiv)


def buttonRL():
    global statusRL
    statusRL = not (statusRL)
    if statusRL and scaleVentil.get():
        schaltenRL(True)
    else:
        schaltenRL(False)
    return


buttonVentilRL = Button(fenster, command=buttonRL, image=bildVentil, compound=TOP)
buttonVentilRL.configure(width=80, height=80, state=DISABLED, anchor=CENTER)
buttonRL_window = fenster.create_window(525, 755, window=buttonVentilRL)


def buttonVL():
    global statusVL
    statusVL = not (statusVL)
    if statusVL and scaleVentil.get():
        schaltenVL(True)
    else:
        schaltenVL(False)
    return


buttonVentilVL = Button(fenster, command=buttonVL, image=bildVentil, compound=TOP)
buttonVentilVL.configure(width=80, height=80, state=DISABLED, anchor=CENTER)
buttonVl_window = fenster.create_window(905, 755, window=buttonVentilVL)


def buttonPumpe():
    global statusPumpe
    if not (scaleZirk.get()):
        statusPumpe = not (statusPumpe)
        if statusPumpe and scaleVentil.get():
            schaltenPumpe(True)
        else:
            schaltenPumpe(False)
    return


buttonVentilPumpe = Button(fenster, command=buttonPumpe, image=bildPumpe, compound=TOP)
buttonVentilPumpe.configure(width=80, height=80, state=DISABLED, anchor=CENTER)
buttonPumpe_window = fenster.create_window(715, 550, window=buttonVentilPumpe)


# --------------------------------------------------Einstellungsfenster-------------***************************
def fensterEinstellungen():
    global sollVL, istVL, sollRL, istRL, differenz, meniskus, scaleVakuum, scaleDruckluft, scaleDruckLos
    fenster = Toplevel(root)
    fenster.title('Einstellungen')
    fenster.geometry('1100x700+300+150')
    fenstKlein = Canvas(fenster, bd=0, width=1080, height=680, bg=farbeBack)
    fenster.configure(width=80, height=800)
    fenstKlein.pack()
    # Hintergrundfelder
    fenstKlein.create_rectangle(20, 20, 295, 235, fill=farbeFront)
    fenstKlein.create_rectangle(315, 20, 700, 235, fill=farbeFront)
    fenstKlein.create_rectangle(720, 20, 1060, 235, fill=farbeFront)
    fenstKlein.create_rectangle(315, 255, 700, 660, fill=farbeFront)
    fenstKlein.create_rectangle(720, 255, 1060, 660, fill=farbeFront)

    def buttonZureckDef():
        global sollVL, sollRL
        fenster.destroy()
        # werteFenster()
        schreiben = basics.iniSchreiben('allVorgaben.ini', 'sollVL', sollVL)
        schreiben = basics.iniSchreiben('allVorgaben.ini', 'sollRL', sollRL)

    # Fenster schliessen
    buttonZurueck = Button(fenstKlein, image=bildKreuz, compound=TOP)
    buttonZurueck.configure(width=80, height=80, anchor=CENTER, command=buttonZureckDef)
    buttonZurueck_window = fenstKlein.create_window(200, 120, window=buttonZurueck)

    # Wertefelder
    fenstKlein.create_rectangle(350, 75, 450, 125, fill=farbeWerte)
    fenstKlein.create_text(450 + schriftOff, 100, text='mbar Sollwert', fill=farbeText, font=schrift2, anchor='w')
    labelSollVL = fenstKlein.create_text(450 - schriftOff, 100, text=sollVL, fill=farbeText, font=schriftWerte,
                                         anchor='e')

    fenstKlein.create_rectangle(350, 150, 450, 200, fill=farbeWerte)
    fenstKlein.create_text(450 + schriftOff, 175, text='mbar Istwert', fill=farbeText, font=schrift2, anchor='w')
    labelIstVL = fenstKlein.create_text(450 - schriftOff, 175, text=istVL, fill=farbeText, font=schriftWerte,
                                        anchor='e')

    fenstKlein.create_rectangle(745, 75, 845, 125, fill=farbeWerte)
    fenstKlein.create_text(845 + schriftOff, 100, text='mbar Sollwert', fill=farbeText, font=schrift2, anchor='w')
    labelSollRL = fenstKlein.create_text(845 - schriftOff, 100, text=sollRL, fill=farbeText, font=schriftWerte,
                                         anchor='e')

    fenstKlein.create_rectangle(745, 150, 845, 200, fill=farbeWerte)
    fenstKlein.create_text(845 + schriftOff, 175, text='mbar Istwert', fill=farbeText, font=schrift2, anchor='w')
    labelIstRL = fenstKlein.create_text(845 - schriftOff, 175, text=istRL, fill=farbeText, font=schriftWerte,
                                        anchor='e')

    fenstKlein.create_text(20 + schriftOff, 40, text='Farbsystem', fill=farbeText, font=schrift1, anchor='w')
    fenstKlein.create_text(325 + schriftOff, 40, text='Vakuumsystem VL', fill=farbeText, font=schrift1, anchor='w')
    fenstKlein.create_text(720 + schriftOff, 40, text='Vakuumsystem RL', fill=farbeText, font=schrift1, anchor='w')
    fenstKlein.create_text(350 + schriftOff, 275, text='Meniskus', fill=farbeText, font=schrift1, anchor='w')
    fenstKlein.create_text(510 + schriftOff, 275, text='Differenz', fill=farbeText, font=schrift1, anchor='w')

    # Erklaerung
    fenstKlein.create_text(100, 450, text='Meniskus', fill='lightgrey', font=schrift1, anchor='center')
    fenstKlein.create_text(100, 280, text='SollRL', fill='lightgrey', font=schrift1, anchor='center')
    fenstKlein.create_text(100, 620, text='SollVL', fill='lightgrey', font=schrift1, anchor='center')
    fenstKlein.create_text(200, 445, text='D\ni\nf\nf\ne\nr\ne\nn\nz', fill='lightgrey', font=schrift1,
                           anchor='center')
    fenstKlein.create_line(200, 580, 200, 620, fill='white', width=3)
    fenstKlein.create_line(200, 280, 200, 320, fill='white', width=3)
    fenstKlein.create_line(190, 280, 210, 280, fill='white', width=3)
    fenstKlein.create_line(190, 620, 210, 620, fill='white', width=3)

    # Scales
    def scaleMeniskusDef(wert):  # Uebergabe ist String
        global sollVL, sollRL
        meniskus = float(wert)
        differenz = sollRL - sollVL
        sollVL = round(meniskus + (differenz / 2), 1)
        sollRL = round(meniskus - (differenz / 2), 1)
        schreiben = basics.iniSchreiben('allSoll.ini', 'sollVL', sollVL)
        schreiben = basics.iniSchreiben('allSoll.ini', 'sollRL', sollRL)
        fenstKlein.itemconfigure(labelSollVL, text=sollVL)  # Aktualisiere Text in Textfeld
        fenstKlein.itemconfigure(labelSollRL, text=sollRL)
        return

    scaleMeniskus = Scale(fenstKlein, variable=sollVL, digits=3, resolution=0.1, tickinterval=10)
    scaleMeniskus.configure(bg="Grey", orient=VERTICAL, width=40, length=340, sliderlength=20, font=schrift2,
                            command=scaleMeniskusDef,
                            activebackground="Grey", relief=FLAT, from_=-60, to_=0, troughcolor=farbeBack)
    fenstKlein.create_window(350, 470, anchor=W, window=scaleMeniskus)
    scaleMeniskus.set(sollVL)

    def scaleDifferenzDef(wert):  # Uebergabe ist String
        global sollVL, sollRL
        differenz = float(wert)
        meniskus = sollRL - 0.5 * (sollRL - sollVL)
        sollVL = round(meniskus + (differenz / 2), 1)
        sollRL = round(meniskus - (differenz / 2), 1)
        schreiben = basics.iniSchreiben('allSoll.ini', 'sollVL', sollVL)
        schreiben = basics.iniSchreiben('allSoll.ini', 'sollRL', sollRL)
        fenstKlein.itemconfigure(labelSollVL, text=sollVL)  # Aktualisiere Text in Textfeld
        fenstKlein.itemconfigure(labelSollRL, text=sollRL)
        return

    differenz = sollRL - sollVL
    scaleDifferenz = Scale(fenstKlein, variable=differenz, digits=3, resolution=0.1, tickinterval=5, )
    scaleDifferenz.configure(bg="Grey", orient=VERTICAL, width=40, length=340, sliderlength=20, font=schrift2,
                             command=scaleDifferenzDef,
                             activebackground="Grey", relief=FLAT, from_=30, to_=0, troughcolor=farbeBack)
    fenstKlein.create_window(510, 470, anchor=W, window=scaleDifferenz, )
    scaleDifferenz.set(differenz)

    # Scale Vakuum
    def scaleVakuumDef(wert):
        global scaleVakuum
        scaleVakuum = wert
        # regelventile.vakuumventile(wert)
        if wert == '1':
            scaleVakuumFarbe1 = 'darkgreen'
        else:
            scaleVakuumFarbe1 = 'darkred'
        scaleVakuumFen.configure(troughcolor=scaleVakuumFarbe1)
        print('scaleVakuum ', scaleVakuumFarbe1)
        return

    scaleVakuumFarbe = 'darkgreen'
    scaleVakuumFen = Scale(fenstKlein, variable=scaleVakuum, bg="Grey", orient=HORIZONTAL, width=40,
                           sliderlength=50)
    scaleVakuumFen.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0,
                             troughcolor=scaleVakuumFarbe, command=scaleVakuumDef)
    fenstKlein.create_window(745, 320, anchor=W, window=scaleVakuumFen)
    fenstKlein.create_text(860, 320, text='Vakuum ein/aus', fill=farbeText, font=schrift1, anchor='w')
    scaleVakuumFen.set(int(scaleVakuum))

    # Scale Drucklos
    def scaleDruckLosDef(wert):
        global scaleDruckLos
        scaleDruckLos = wert
        # regelventile.druckLos(wert)
        if wert == '1':
            scaleDruckLosFarbe = 'darkgreen'
        else:
            scaleDruckLosFarbe = 'darkred'
        scaleDruckLosFen.configure(troughcolor=scaleDruckLosFarbe)
        print('DruckLos', wert, type(wert))
        return

    scaleDruckLosFarbe = 'darkred'
    scaleDruckLosFen = Scale(fenstKlein, bg="Grey", orient=HORIZONTAL, width=40,
                             sliderlength=50)
    scaleDruckLosFen.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0,
                               troughcolor=scaleDruckLosFarbe, command=scaleDruckLosDef)
    fenstKlein.create_window(745, 400, anchor=W, window=scaleDruckLosFen)
    fenstKlein.create_text(860, 400, text='DruckLos ein/aus', fill=farbeText, font=schrift1, anchor='w')
    scaleDruckLosFen.set(scaleDruckLos)

    # Scale Druckluft
    def scaleDruckluftDef(wert):
        global scaleDruckluft
        # regelventile.druckluftventil(wert)
        scaleDruckluft = wert
        if wert == '1':
            scaleDruckluftFarbe = 'darkgreen'
        else:
            scaleDruckluftFarbe = 'darkred'
        scaleDruckluftFen.configure(troughcolor=scaleDruckluftFarbe)
        print('Druckluft', wert, type(wert))
        return

    scaleDruckluftFarbe = 'darkred'
    scaleDruckluftFen = Scale(fenstKlein, bg="Grey", orient=HORIZONTAL, width=40,
                              sliderlength=50)
    scaleDruckluftFen.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0,
                                troughcolor=scaleDruckluftFarbe, command=scaleDruckluftDef)
    fenstKlein.create_window(745, 480, anchor=W, window=scaleDruckluftFen)
    fenstKlein.create_text(860, 480, text='Druckluft ein/aus', fill=farbeText, font=schrift1, anchor='w')
    scaleDruckluftFen.set(scaleDruckluft)


buttonEinstellungen = Button(fenster, text="Einstellungen", command=lambda: fensterEinstellungen())
buttonEinstellungen.configure(width=15, height=2, fg='White', bg='Grey', relief=RAISED, state=ACTIVE, font=schrift2)
buttonFenster_window = fenster.create_window(1140, 100, anchor=W, window=buttonEinstellungen)

# Hintergrundfelder
fenster.create_rectangle(20, 20, 295, 235, fill=farbeFront)
fenster.create_rectangle(315, 20, 700, 235, fill=farbeFront)
fenster.create_rectangle(720, 20, 1100, 235, fill=farbeFront)
fenster.create_rectangle(1120, 20, 1460, 235, fill=farbeFront)
fenster.create_rectangle(20, 255, 295, 625, fill=farbeFront)
fenster.create_rectangle(315, 255, 1460, 860, fill=farbeFront)

fenster.create_text(20 + schriftOff, 40, text='Farbsystem', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(325 + schriftOff, 40, text='Vakuumsystem VL', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(720 + schriftOff, 40, text='Vakuumsystem RL', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(1120 + schriftOff, 40, text='Optionen', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(20 + schriftOff, 275, text='Spuelen', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(1175, 700, text='Ventile manuell steuern', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(1175, 760, text='Zirkulation sperren', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(1175, 820, text='Sensoren deaktivieren', fill=farbeText, font=schrift1, anchor='w')
fenster.pack()

# Wertefelder
fenster.create_rectangle(350, 75, 450, 125, fill=farbeWerte)
fenster.create_text(450 + schriftOff, 100, text='mbar Sollwert', fill=farbeText, font=schrift2, anchor='w')
wertSollVL = fenster.create_text(450 - schriftOff, 100, text=sollVL, fill=farbeText, font=schriftWerte,
                                 anchor='e')

fenster.create_rectangle(350, 150, 450, 200, fill=farbeWerte)
fenster.create_text(450 + schriftOff, 175, text='mbar Istwert', fill=farbeText, font=schrift2, anchor='w')
wertIstVL = fenster.create_text(450 - schriftOff, 175, text=istVL, fill=farbeText, font=schriftWerte, anchor='e')

fenster.create_rectangle(745, 75, 845, 125, fill=farbeWerte)
fenster.create_text(845 + schriftOff, 100, text='mbar Sollwert', fill=farbeText, font=schrift2, anchor='w')
wertSollRL = fenster.create_text(845 - schriftOff, 100, text=sollRL, fill=farbeText, font=schriftWerte,
                                 anchor='e')

fenster.create_rectangle(745, 150, 845, 200, fill=farbeWerte)
fenster.create_text(845 + schriftOff, 175, text='mbar Istwert', fill=farbeText, font=schrift2, anchor='w')
wertIstRL = fenster.create_text(845 - schriftOff, 175, text=istRL, fill=farbeText, font=schriftWerte, anchor='e')

dy = 45  # Fuellstand links
fenster.create_rectangle(350, 525, 410, 575, fill=farbeWerte)
fenster.create_text(410 + schriftOff, 550, text='%', fill=farbeText, font=schrift2, anchor='w')
wertFuellstandRL = fenster.create_text(410 - schriftOff, 550, text=fuellstandRL, fill=farbeText, font=schriftWerte,
                                       anchor='e')

dx = 650  # Fuellstand rechts
fenster.create_rectangle(350 + dx, 525, 410 + dx, 575, fill=farbeWerte)
fenster.create_text(410 + dx + schriftOff, 550, text='%', fill=farbeText, font=schrift2, anchor='w')
wertFuellstandVL = fenster.create_text(410 + dx - schriftOff, 550, text=fuellstandVL, fill=farbeText, font=schriftWerte,
                                       anchor='e')

dx = 335  # Pumpenanzeige
dy = 100
fenster.create_rectangle(350 + dx, 525 + dy, 410 + dx, 575 + dy, fill=farbeWerte)
fenster.create_text(410 + dx + schriftOff, 550 + dy, text='%', fill=farbeText, font=schrift2, anchor='w')
wertPumpeIst = fenster.create_text(410 + dx - schriftOff, 550 + dy, text=istPumpe, fill=farbeText, font=schriftWerte,
                                   anchor='e')

# Tanks
fenster.create_rectangle(450, 325, 600, 675, fill='white')
fenster.create_rectangle(830, 325, 980, 675, fill='white')
# Leitungen
fenster.create_rectangle(515, 675, 535, 830, fill='Darkgrey', outline='Darkgrey')
fenster.create_rectangle(895, 675, 915, 830, fill='Darkgrey', outline='Darkgrey')
fenster.create_rectangle(515, 275, 535, 325, fill='Darkgrey', outline='Darkgrey')
fenster.create_rectangle(895, 275, 915, 325, fill='Darkgrey', outline='Darkgrey')
fenster.create_rectangle(600, 540, 830, 560, fill='Darkgrey', outline='Darkgrey')
# Druckkopf
fenster.create_rectangle(450, 830, 980, 840, fill='Darkgrey', outline='Darkgrey')
fenster.create_rectangle(605, 730, 825, 830, fill='Darkgrey', outline='Darkgrey')


def task():
    wert = randint(0, 100)
    print(wert)
    global sollVL, istVL, sollRL, istRL
    print(sollVL)

    fenster.itemconfigure(wertSollVL, text=sollVL)  # Aktualisiere Text in Textfeld
    fenster.itemconfigure(wertSollRL, text=sollRL)
    istVL = basics.iniLesen('all_Ist.ini', 'istVL')
    fenster.itemconfigure(wertIstVL, text=istVL)  # Aktualisiere Text in Textfeld
    istVL = basics.iniLesen('all_Ist.ini', 'istRL')
    fenster.itemconfigure(wertIstRL, text=istRL)
    istPumpe = basics.iniLesen('all_Ist.ini', 'istPumpe')
    fenster.itemconfigure(wertPumpeIst, text=istPumpe)
    fuellstandVL = basics.iniLesen('all_Ist.ini', 'fuellstandVL')
    fenster.itemconfigure(wertFuellstandVL, text=fuellstandVL)
    fuellstandRL = basics.iniLesen('all_Ist.ini', 'fuellstandRL')
    fenster.itemconfigure(wertFuellstandRL, text=fuellstandRL)

    # Tank farbig

    if fuellstandRL > fuellstandOEG or fuellstandRL < fuelstandUEG:
        farbeRL = 'darkred'
    else:
        farbeRL = 'darkgreen'
    fenster.create_rectangle(450, 325, 600, 675, fill=farbeRL)
    fuellstandRL = 100 - int(fuellstandRL)
    fenster.create_rectangle(450, 325, 600, 325 + ((300 * fuellstandRL / 100)), fill=farbeTanks)

    if fuellstandVL > fuellstandOEG or fuellstandVL < fuelstandUEG:
        farbeVL = 'darkred'
    else:
        farbeVL = 'darkgreen'
    fenster.create_rectangle(830, 325, 980, 675, fill=farbeVL)
    fuellstandVL = 100 - int(fuellstandVL)
    fenster.create_rectangle(830, 325, 980, 325 + ((300 * fuellstandVL / 100)), fill=farbeTanks)
    # fenster.create_rectangle(830, 325, 980, 675, fill=farbeVL)

    fenster.after(1000, task)  # reschedule event in 1 seconds


# -------------------------Start--------------------------------------------------------------------------
#allRelais.setup()
#task()
root.mainloop()
