import os.path
from tkinter import *
from tkinter import messagebox
import sys
import a_Interface
import a_setup
import basics
import threading
import a_schalter

#Bemerkung für Github
a = sys.executable  # Schutz von import sys vorm Löschen durch automatisch formatieren
b = a
if '/usr/bin' in sys.executable:
    os.chdir(sys.path[0])  # ToDo: Pfad für Bildschirm

if a_setup.systemTest(): # Prüft System und bei Fehler kommt der Abbruch
    a_Interface.stop()
    sys.exit(0)
#print(sys.path)
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
schriftWerte = ('Arial', 25, 'italic')
schriftOff = 10
root = Tk()
root.title('Farbsystem HM')
root.geometry('1500x900+100+50')
fenster = Canvas(root, bd=0, width=1480, height=880, bg=farbeBack)



# Setup-------------------------------------------------------------Setup------------------------------------------
global istVL, istRL, istPumpe, fuellstandVL, fuellstandRL, statusVL, statusRL, sollPumpe

# Werte aus allVorgaben.ini und allSoll.ini einlesen
sollVL = DoubleVar()
istVL = DoubleVar()
sollRL = DoubleVar()
istRL = DoubleVar()
istPumpe = DoubleVar()

statusVL = basics.iniLesen('allVorgaben.ini', 'statusVL')
sollVL = round(float(basics.iniLesen('allVorgaben.ini', 'sollVL')), 1)
statusRL = basics.iniLesen('allVorgaben.ini', 'statusRL')
sollRL = round(float(basics.iniLesen('allVorgaben.ini', 'sollRL')), 1)
sollPumpe = round(float(basics.iniLesen('allVorgaben.ini', 'sollPumpe')), 1)
istPumpe = sollPumpe
statusPumpe = 'Aus'  # Optionen: auto, manuell
statusDruck = basics.iniLesen('allVorgaben.ini', 'statusDruck')
sollDruck = round(float(basics.iniLesen('allVorgaben.ini', 'sollDruck')), 1)

# Ist-Werte von Füllstandsregler

fuellstandVL = round(float(basics.iniLesen('allVorgaben', 'fuellstandVL')), 1)
fuellstandRL = round(float(basics.iniLesen('allVorgaben', 'fuellstandRL')), 1)

# Schalter
scaleVakuum = int(basics.iniLesen('allVorgaben.ini', 'scaleVakuum'))  # Schaltervorgaben
scaleDruckLos = basics.iniLesen('allVorgaben.ini', 'scaleDruckLos')
scaleDruckluft = basics.iniLesen('allVorgaben.ini', 'scaleDruckluft')

# Eingriffsgrenzen
fuellstandOEG = int(basics.iniLesen('allVorgaben.ini', 'FuellstandOEG'))
fuelstandUEG = int(basics.iniLesen('allVorgaben.ini', 'FuellstandUEG'))
quadFarbeVL=fenster.create_rectangle(450, 325, 600, 675, fill=farbeVL)
quadFarbeRL=fenster.create_rectangle(450, 325, 600, 675, fill=farbeTanks)

# Definition der Images fuer Buttons
bildVentilAuf = PhotoImage(file='Ventil-auf.png')
bildVentilZu = PhotoImage(file='Ventil-zu.png')
bildVentil = bildVentilZu
bildPumpeAuf = PhotoImage(file='Pumpe-auf.png')
bildPumpeZu = PhotoImage(file='Pumpe-zu.png')
bildPumpe = bildPumpeZu
bildKreuz = PhotoImage(file='Kreuz.png')


# --------------------------------------------------Hochfahren der Anlage---------------------------------------

# Schalten von Ventil und Zirkulation----------------------------------------------------------------------------

def schaltenSollVl(wert):
    global sollVL
    sollVL = wert
    basics.iniSchreiben('allVorgaben.ini', 'sollVL', wert)
    a_Interface.regler('reglerVL', wert)


def schaltenSollRl(wert):
    global sollRL
    sollRL = wert
    basics.iniSchreiben('allVorgaben.ini', 'sollRL', wert)
    a_Interface.regler('reglerRL', wert)


def schaltenRL(wert):
    global statusRL
    statusRL = wert
    if wert:
        bildVentil = bildVentilAuf
        a_Interface.schalter('ventilRL', True)
    else:
        bildVentil = bildVentilZu
        a_Interface.schalter('ventilRL', False)
    buttonVentilRL.configure(image=bildVentil)
    #print('Ventil RL:', statusRL)


def schaltenVL(wert):
    global statusVL
    statusVL = wert
    if wert:
        bildVentil = bildVentilAuf
        a_Interface.schalter('ventilVL', True)
    else:
        bildVentil = bildVentilZu
        a_Interface.schalter('ventilVL', False)
    buttonVentilVL.configure(image=bildVentil)
    #print('Ventil VL:', statusVL)


def schaltenPumpe(wert) -> object:
    global sollPumpe, statusPumpe

    if wert:
        bildPumpe = bildPumpeAuf
        a_Interface.schalter('pumpeInk', True)
        statusPumpe = 'auto'
    else:
        bildPumpe = bildPumpeZu
        a_Interface.schalter('pumpeInk', False)
        statusPumpe = 'aus'

    #print('a_Fenster schaltenPumpe: wert ', wert)
    buttonVentilPumpe.configure(image=bildPumpe)



def schaltenLicht(wert):
    if wert:
        a_Interface.schalter('Licht', True)
    else:
        a_Interface.schalter('Licht', False)
    #print('Licht:', wert)


def purgen(wert) -> object:

    global sollPumpe
    purgenThread=threading.Thread(target=a_Interface.purgen,args=(wert, sollPumpe))
    purgenThread.start()

def schaltenDrucklos(wert):
    if wert:
        schaltenPumpe(False)
        a_Interface.regler('druckPurgen', 0)
        a_Interface.schalter('purgenVL', True)
        a_Interface.schalter('purgenRL', True)

    else:
        schaltenPumpe(True)
        a_Interface.schalter('purgenVL', False)
        a_Interface.schalter('purgenRL', False)


# Schiebeschalter
scaleFarbe = 'Red'
scaleFarbeLicht = 'Darkred'
scaleFarbeVentil = 'Darkred'
scaleFarbeZirk = 'Darkred'
buttonFarbe = 'Blue'


def scaleEinCommand(wertStr):  # Uebergabe ist String
    global statusPumpe
    wert = int(wertStr)
    if wert == 1:
        scaleFarbe = 'Green'
        buttonVentilNormal.configure(state=ACTIVE)
        buttonVentilIntensiv.configure(state=ACTIVE)
        buttonVentilmaxVL.configure(state=ACTIVE)
        buttonVentilmaxRL.configure(state=ACTIVE)
        buttonVakuum.configure(state=ACTIVE)
        buttonPumpeFenster.configure(state=ACTIVE)

        schaltenVL(True)
        schaltenSollVl(sollVL)
        schaltenRL(True)
        schaltenSollRl(sollRL)
        schaltenPumpe(True)
        schaltenSollRl(sollRL)

        a_Interface.start()


    else:
        scaleFarbe = 'Darkred'
        scaleVentil.set(0)
        scaleFarbeVentil = 'Darkred'
        buttonVentilNormal.configure(state=DISABLED)
        buttonVentilIntensiv.configure(state=DISABLED)
        buttonVentilmaxVL.configure(state=DISABLED)
        buttonVentilmaxRL.configure(state=DISABLED)
        scaleVentilDef.configure(troughcolor=scaleFarbeVentil)
        scaleZirk.set(0)
        scaleFarbeZirk = 'Darkred'
        scaleZirkDef.configure(troughcolor=scaleFarbeZirk)
        scaleLicht.set(0)
        scaleFarbeLicht = 'Darkred'
        scaleLichtDef.configure(troughcolor=scaleFarbeLicht)
        buttonVentilRL.configure(state=DISABLED)
        buttonVentilVL.configure(state=DISABLED)
        buttonVentilPumpe.configure(state=DISABLED)
        buttonVakuum.configure(state=DISABLED)
        buttonPumpeFenster.configure(state=DISABLED)

        schaltenVL(False)
        schaltenRL(False)
        schaltenPumpe(False)

        a_Interface.stop()

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
scaleZirkDef.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0,
                       troughcolor=scaleFarbeZirk,
                       command=scaleZirkCommand)
scale_window_Zirk = fenster.create_window(1065, 760, anchor=W, window=scaleZirkDef)


def scaleLichtCommand(wertStr):  # Uebergabe ist String
    wert = int(wertStr)
    #print('Licht\t', wert)
    if wert == 1 and scaleEin.get() == 1:
        scaleFarbe1 = 'Green'

    else:
        scaleFarbe1 = 'Darkred'
        scaleLicht.set(0)
    schaltenLicht(not (wert))
    scaleLichtDef.configure(troughcolor=scaleFarbe1)
    return


scaleLicht = DoubleVar()
scaleLichtDef = Scale(fenster, variable=scaleLicht, bg="Grey", orient=HORIZONTAL, width=40, sliderlength=50)
scaleLichtDef.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0, state=ACTIVE,
                        troughcolor=scaleFarbeLicht, command=scaleLichtCommand)
scale_window_Licht = fenster.create_window(1065, 820, anchor=W, window=scaleLichtDef)


# Button-----------------------------------------------------------------------------------------button

def exitDef():
    global fuellstandVL, fuellstandRL, sollPumpe
    #print('Ende')
    frage = messagebox.askokcancel('Pi4Ink beenden', 'Wollen Sie wirklich Pi4Ink beenden?')
    if frage:
        a_Interface.stop()
        basics.iniSchreiben('allVorgaben.ini', 'fuellstandVL', fuellstandVL)
        basics.iniSchreiben('allVorgaben.ini', 'fuellstandRVL', fuellstandRL)
        basics.iniSchreiben('allVorgaben.ini', 'sollPumpe', sollPumpe)
        root.destroy()


# Fenster schliessen
buttonEnde = Button(fenster, text="Ende", command=exitDef, font=schrift2, )
buttonEnde.configure(width=8, height=1, fg='White', bg='Darkgrey', relief=RAISED, state=ACTIVE)
buttonZurueck_window = fenster.create_window(200, 175, anchor=CENTER, window=buttonEnde)


def buttonNormal():  # spülen normal
    global sollVL, sollRL, sollPumpe, statusPumpe
    wert = scaleEin.get()
    #print('Wert', wert)
    if wert == 1:
        purgen('spuelen')
    return


buttonVentilNormal = Button(fenster, text="normal", command=buttonNormal, font=schrift2)
buttonVentilNormal.configure(width=15, height=3, fg='White', bg='Grey', relief=RAISED, state=DISABLED)
buttonNormal_window = fenster.create_window(158, 365, anchor=CENTER, window=buttonVentilNormal)


def buttonintensiv():
    global sollVL, sollRL, sollPumpe, statusPumpe
    wert = scaleEin.get()
    #print('Wert', wert)
    if wert == 1:
        purgen('intensiv')
    return


buttonVentilIntensiv = Button(fenster, text="intensiv", command=buttonintensiv, font=schrift2, )
buttonVentilIntensiv.configure(width=15, height=3, fg='White', bg='Grey', relief=RAISED, state=DISABLED)
buttonintensiv_window = fenster.create_window(158, 500, anchor=CENTER, window=buttonVentilIntensiv)


def buttonmaxVL():
    global sollVL, sollRL, sollPumpe, statusPumpe
    wert = scaleEin.get()
    #print('Wert', wert)
    if wert == 1:
        purgen('maxVL')
    return


buttonVentilmaxVL = Button(fenster, text="maxVL", command=buttonmaxVL, font=schrift2, )
buttonVentilmaxVL.configure(width=7, height=3, fg='White', bg='Grey', relief=RAISED, state=DISABLED)
buttonmaxVL_window = fenster.create_window(97, 635, anchor=CENTER, window=buttonVentilmaxVL)


def buttonmaxRL():
    global sollVL, sollRL, sollPumpe, statusPumpe
    wert = scaleEin.get()
    #print('Wert', wert)
    if wert == 1:
        purgen('maxRL')
    return


buttonVentilmaxRL = Button(fenster, text="maxRL", command=buttonmaxRL, font=schrift2, )
buttonVentilmaxRL.configure(width=7, height=3, fg='White', bg='Grey', relief=RAISED, state=DISABLED)
buttonmaxRL_window = fenster.create_window(218, 635, anchor=CENTER, window=buttonVentilmaxRL)


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
buttonRL_window = fenster.create_window(955, 755, window=buttonVentilRL)


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
buttonVl_window = fenster.create_window(575, 755, window=buttonVentilVL)


def buttonPumpe():
    global statusPumpe
    #print('statusPumpe start', statusPumpe)
    if not (scaleZirk.get()):
        if statusPumpe == 'aus' and scaleVentil.get():
            schaltenPumpe('True')
        else:
            schaltenPumpe(False)
    #print('statusPumpe ende', statusPumpe)


buttonVentilPumpe = Button(fenster, command=buttonPumpe, image=bildPumpe, compound=TOP)
buttonVentilPumpe.configure(width=80, height=80, state=DISABLED, anchor=CENTER)
buttonPumpe_window = fenster.create_window(765, 550, window=buttonVentilPumpe)


def pumpeFensterDef():
    global sollPumpe, statusPumpe
    fenster = Toplevel(root)
    fenster.wm_overrideredirect(True)
    fenster.geometry('150x450+805+410')
    fenstKlein = Canvas(fenster, bd=0, width=400, height=440, bg=farbeBack)
    fenstKlein.pack()

    statusPumpe = 'manuell'

    def scaleSollPumpeDef(wert):  # Uebergabe ist String
        global sollPumpe
        sollPumpe = float(wert)
        basics.iniSchreiben('allVorgaben.ini', 'sollPumpe', sollPumpe)
        #print(sollPumpe)

    sollPumpeAnzeige = round(sollPumpe, 1)
    scaleSollPumpe = Scale(fenstKlein, variable=sollPumpeAnzeige, digits=3, resolution=0.1, tickinterval=10)
    scaleSollPumpe.configure(bg="Grey", orient=VERTICAL, width=80, length=340, sliderlength=80, font=schrift2,
                             command=scaleSollPumpeDef,
                             activebackground="Grey", relief=FLAT, from_=100, to_=0, troughcolor=farbeBack)
    fenstKlein.create_window(90, 170, anchor=CENTER, window=scaleSollPumpe)
    scaleSollPumpe.set(sollPumpeAnzeige)

    def buttonPumpeExitDef():
        global statusPumpe
        statusPumpe = 'auto'
        fenster.destroy()

    buttonPumpeExit = Button(fenster, command=buttonPumpeExitDef, image=bildKreuz, compound=TOP)
    buttonPumpeExit.configure(width=150, height=120, state=ACTIVE, anchor=CENTER)
    buttonPumpe_window = fenstKlein.create_window(80, 393, window=buttonPumpeExit)


# SollPumpe Scale
buttonPumpeFenster = Button(fenster, text='Pumpenleistung', command=pumpeFensterDef, font=schrift2, )
buttonPumpeFenster.configure(width=15, height=1, fg='White', bg='Grey', relief=RAISED, state=ACTIVE)
pumpeFenster_window = fenster.create_window(1140, 150, anchor=W, window=buttonPumpeFenster)

# Setup
buttonSetup = Button(fenster, text='Setup', command=lambda: a_setup.start(root), font=schrift2, )
buttonSetup.configure(width=7, height=1, fg='White', bg='Grey', relief=RAISED, state=ACTIVE)
Setup_window = fenster.create_window(1140, 200, anchor=W, window=buttonSetup)

# Schalter1
buttonSchalter1 = Button(fenster, text='Ventile', command=lambda: a_schalter.start(root), font=schrift2, )
buttonSchalter1.configure(width=7, height=1, fg='White', bg='Grey', relief=RAISED, state=ACTIVE)
Schalter1_window = fenster.create_window(1260, 200, anchor=W, window=buttonSchalter1)


# --------------------------------------------------Einstellungsfenster-------------***************************
def fensterVakuum():
    global sollVL, istVL, sollRL, istRL, scaleVakuum, scaleDruckluft, scaleDruckLos
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
        schaltenSollVl(sollVL)
        schaltenSollRl(sollRL)

    # Fenster schliessen
    buttonZurueck = Button(fenstKlein, image=bildKreuz, compound=TOP)
    buttonZurueck.configure(width=80, height=80, anchor=CENTER, command=buttonZureckDef)
    buttonZurueck_window = fenstKlein.create_window(200, 120, window=buttonZurueck)

    # Wertefelder
    fenstKlein.create_rectangle(745, 75, 845, 125, fill=farbeWerte)
    fenstKlein.create_text(845 + schriftOff, 100, text='mbar Sollwert', fill=farbeText, font=schrift2, anchor='w')
    labelSollRL = fenstKlein.create_text(845 - schriftOff, 100, text=sollRL, fill=farbeText, font=schriftWerte,
                                         anchor='e')

    fenstKlein.create_rectangle(745, 150, 845, 200, fill=farbeWerte)
    fenstKlein.create_text(845 + schriftOff, 175, text='mbar Istwert', fill=farbeText, font=schrift2, anchor='w')
    labelIstRL = fenstKlein.create_text(845 - schriftOff, 175, text=istRL, fill=farbeText, font=schriftWerte,
                                        anchor='e')

    fenstKlein.create_rectangle(350, 75, 450, 125, fill=farbeWerte)
    fenstKlein.create_text(450 + schriftOff, 100, text='mbar Sollwert', fill=farbeText, font=schrift2, anchor='w')
    labelSollVL = fenstKlein.create_text(450 - schriftOff, 100, text=sollVL, fill=farbeText, font=schriftWerte,
                                         anchor='e')

    fenstKlein.create_rectangle(350, 150, 450, 200, fill=farbeWerte)
    fenstKlein.create_text(450 + schriftOff, 175, text='mbar Istwert', fill=farbeText, font=schrift2, anchor='w')
    labelIstVL = fenstKlein.create_text(450 - schriftOff, 175, text=istVL, fill=farbeText, font=schriftWerte,
                                        anchor='e')

    fenstKlein.create_text(20 + schriftOff, 40, text='Farbsystem', fill=farbeText, font=schrift1, anchor='w')
    fenstKlein.create_text(325 + schriftOff, 40, text='Vakuumsystem VL', fill=farbeText, font=schrift1, anchor='w')
    fenstKlein.create_text(720 + schriftOff, 40, text='Vakuumsystem RL', fill=farbeText, font=schrift1, anchor='w')
    fenstKlein.create_text(350 + schriftOff, 275, text='Meniskus', fill=farbeText, font=schrift1, anchor='w')
    fenstKlein.create_text(510 + schriftOff, 275, text='Differenz', fill=farbeText, font=schrift1, anchor='w')

    # Erklaerung
    fenstKlein.create_text(120, 450, text='Meniskus', fill='lightgrey', font=schrift2, anchor='center')
    fenstKlein.create_line(40, 450, 60, 450, fill='white', width=3)
    fenstKlein.create_line(180, 450, 200, 450, fill='white', width=3)
    fenstKlein.create_text(100, 280, text='SollVL', fill='lightgrey', font=schrift2, anchor='center')
    fenstKlein.create_text(100, 620, text='SollRL', fill='lightgrey', font=schrift2, anchor='center')
    fenstKlein.create_text(260, 445, text='D\ni\nf\nf\ne\nr\ne\nn\nz', fill='lightgrey', font=schrift2,
                           anchor='center')
    fenstKlein.create_line(223, 280, 223, 620, fill='white', width=3)
    fenstKlein.create_line(160, 280, 295, 280, fill='white', width=3)
    fenstKlein.create_line(160, 620, 295, 620, fill='white', width=3)

    # Scales
    def scaleMeniskusDef(wert):  # Uebergabe ist String
        global sollVL, sollRL
        meniskus = float(wert)
        differenz = sollRL - sollVL  # TODO: Bei Umrechnung auf mbar ohne Minus
        sollVL = round(meniskus - (differenz / 2), 1)
        sollRL = round(meniskus + (differenz / 2), 1)
        schaltenSollVl(sollVL)
        schaltenSollRl(sollRL)
        fenstKlein.itemconfigure(labelSollVL, text=sollVL)  # Aktualisiere Text in Textfeld
        fenstKlein.itemconfigure(labelSollRL, text=sollRL)
        return

    meniskus = sollRL - 0.5 * (sollRL - sollVL)
    scaleMeniskus = Scale(fenstKlein, variable=meniskus, digits=3, resolution=0.01, tickinterval=20)
    scaleMeniskus.configure(bg="Grey", orient=VERTICAL, width=50, length=340, sliderlength=100, font=schrift2,
                            command=scaleMeniskusDef,
                            activebackground="Grey", relief=FLAT, from_=100, to_=0, troughcolor=farbeBack)
    fenstKlein.create_window(350, 470, anchor=W, window=scaleMeniskus)
    scaleMeniskus.set(meniskus)

    def scaleDifferenzDef(wert):  # Uebergabe ist String
        global sollVL, sollRL
        differenz = float(wert)
        meniskus = sollRL - 0.5 * (sollRL - sollVL)
        sollVL = round(meniskus - (differenz / 2), 1)
        sollRL = round(meniskus + (differenz / 2), 1)
        schaltenSollVl(sollVL)
        schaltenSollRl(sollRL)
        fenstKlein.itemconfigure(labelSollVL, text=sollVL)  # Aktualisiere Text in Textfeld
        fenstKlein.itemconfigure(labelSollRL, text=sollRL)
        return

    differenz = abs(sollRL - sollVL)
    print(differenz)
    scaleDifferenz = Scale(fenstKlein, variable=differenz, digits=3, resolution=0.01, tickinterval=10, )
    scaleDifferenz.configure(bg="Grey", orient=VERTICAL, width=50, length=340, sliderlength=100, font=schrift2,
                             command=scaleDifferenzDef,
                             activebackground="Grey", relief=FLAT, from_=40, to_=-10, troughcolor=farbeBack)
    fenstKlein.create_window(510, 470, anchor=W, window=scaleDifferenz, )
    scaleDifferenz.set(differenz)

    # Scale Vakuum
    def scaleVakuumDef(wert):
        global scaleVakuum, sollVL, sollRL
        scaleVakuum = wert
        a_Interface.regler('reglerVL', 0)
        a_Interface.regler('reglerRL', 0)
        # regelventile.vakuumventile(wert)
        if wert == '1':
            scaleVakuumFarbe1 = 'darkgreen'
        else:
            scaleVakuumFarbe1 = 'darkred'
            a_Interface.regler('reglerVL', sollVL)
            a_Interface.regler('reglerRL', sollRL)
        scaleVakuumFen.configure(troughcolor=scaleVakuumFarbe1)
        print('scaleVakuum ', scaleVakuumFarbe1)
        return

    scaleVakuumFarbe = 'darkred'
    scaleVakuumFen = Scale(fenstKlein, variable=scaleVakuum, bg="Grey", orient=HORIZONTAL, width=40,
                           sliderlength=50)
    scaleVakuumFen.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0,
                             troughcolor=scaleVakuumFarbe, command=scaleVakuumDef)
    fenstKlein.create_window(745, 320, anchor=W, window=scaleVakuumFen)
    fenstKlein.create_text(860, 320, text='Vakuum ein/aus', fill=farbeText, font=schrift2, anchor='w')
    scaleVakuumFen.set(int(scaleVakuum))

    # Scale Drucklos
    def scaleDruckLosDef(wert):
        global scaleDruckLos
        scaleDruckLos = wert
        # regelventile.druckLos(wert)
        if wert == '1':
            scaleDruckLosFarbe = 'darkgreen'
            schaltenDrucklos(True)
        else:
            scaleDruckLosFarbe = 'darkred'
            schaltenDrucklos(False)
        scaleDruckLosFen.configure(troughcolor=scaleDruckLosFarbe)
        print('DruckLos', wert, type(wert))
        return

    scaleDruckLosFarbe = 'darkred'
    scaleDruckLosFen = Scale(fenstKlein, bg="Grey", orient=HORIZONTAL, width=40,
                             sliderlength=50)
    scaleDruckLosFen.configure(activebackground="Grey", relief=FLAT, from_=0, to_=1, showvalue=0,
                               troughcolor=scaleDruckLosFarbe, command=scaleDruckLosDef)
    fenstKlein.create_window(745, 400, anchor=W, window=scaleDruckLosFen)
    fenstKlein.create_text(860, 400, text='DruckLos ein/aus', fill=farbeText, font=schrift2, anchor='w')
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
    fenstKlein.create_text(860, 480, text='Druckluft ein/aus', fill=farbeText, font=schrift2, anchor='w')
    scaleDruckluftFen.set(scaleDruckluft)


buttonVakuum = Button(fenster, text="Vakuum", command=lambda: fensterVakuum())
buttonVakuum.configure(width=15, height=1, fg='White', bg='Grey', relief=RAISED, state=ACTIVE, font=schrift2)
buttonFenster_window = fenster.create_window(1140, 100, anchor=W, window=buttonVakuum)

# Hintergrundfelder
fenster.create_rectangle(20, 20, 295, 235, fill=farbeFront)
fenster.create_rectangle(315, 20, 700, 235, fill=farbeFront)
fenster.create_rectangle(720, 20, 1100, 235, fill=farbeFront)
fenster.create_rectangle(1120, 20, 1460, 235, fill=farbeFront)
fenster.create_rectangle(20, 255, 295, 860, fill=farbeFront)
fenster.create_rectangle(315, 255, 1460, 860, fill=farbeFront)

fenster.create_text(20 + schriftOff, 40, text='Farbsystem', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(720 + schriftOff, 40, text='Vakuumsystem RL', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(325 + schriftOff, 40, text='Vakuumsystem VL', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(1120 + schriftOff, 40, text='Einstellungen', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(20 + schriftOff, 275, text='Spuelen', fill=farbeText, font=schrift1, anchor='w')
fenster.create_text(1175, 700, text='Ventile manuell steuern', fill=farbeText, font=schrift2, anchor='w')
fenster.create_text(1175, 760, text='Zirkulation sperren', fill=farbeText, font=schrift2, anchor='w')
fenster.create_text(1175, 820, text='Licht aus', fill=farbeText, font=schrift2, anchor='w')
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

dy = 45  # Fuellstand RL
dx = 700
fenster.create_rectangle(350 + dx, 525, 450 + dx, 575, fill=farbeWerte)
fenster.create_text(450 + dx + schriftOff, 550, text='%', fill=farbeText, font=schrift2, anchor='w')
wertFuellstandRL = fenster.create_text(455 + dx - schriftOff, 550, text=fuellstandRL, fill=farbeText,
                                       font=schriftWerte,
                                       anchor='e')

dx = 0  # Fuellstand VL
fenster.create_rectangle(350 + dx, 525, 450 + dx, 575, fill=farbeWerte)
fenster.create_text(450 + dx + schriftOff, 550, text='%', fill=farbeText, font=schrift2, anchor='w')
wertFuellstandVL = fenster.create_text(455 + dx - schriftOff, 550, text=fuellstandVL, fill=farbeText,
                                       font=schriftWerte, anchor='e')

dx = 385  # Pumpenanzeige
dy = 100
fenster.create_rectangle(325 + dx, 525 + dy, 435 + dx, 575 + dy, fill=farbeWerte)
fenster.create_text(435 + dx + schriftOff, 550 + dy, text='%', fill=farbeText, font=schrift2, anchor='w')
wertPumpeIst = fenster.create_text(435 + dx - schriftOff, 550 + dy, text=istPumpe, fill=farbeText,
                                   font=schriftWerte,
                                   anchor='e')

# Tanks
dx = 50
fenster.create_rectangle(450 + dx, 325, 600 + dx, 675, fill='white')
fenster.create_rectangle(830 + dx, 325, 980 + dx, 675, fill='white')
# Leitungen
fenster.create_rectangle(515 + dx, 675, 535 + dx, 830, fill='Darkgrey', outline='Darkgrey')
fenster.create_rectangle(895 + dx, 675, 915 + dx, 830, fill='Darkgrey', outline='Darkgrey')
fenster.create_rectangle(515 + dx, 275, 535 + dx, 325, fill='Darkgrey', outline='Darkgrey')
fenster.create_rectangle(895 + dx, 275, 915 + dx, 325, fill='Darkgrey', outline='Darkgrey')
fenster.create_rectangle(600 + dx, 540, 830 + dx, 560, fill='Darkgrey', outline='Darkgrey')
# Druckkopf
fenster.create_rectangle(450 + dx, 830, 980 + dx, 840, fill='Darkgrey', outline='Darkgrey')
fenster.create_rectangle(605 + dx, 730, 825 + dx, 830, fill='Darkgrey', outline='Darkgrey')


def reglerVakuumpumpe() -> object:
    spannung = a_Interface.adc_mess('vakuum')
    sollVakuum = 0
    if spannung < 10:
        sollVakuum = int(basics.iniLesen('allVorgaben.ini', 'niedrigVakuum'))
    else:
        sollVakuum = int(basics.iniLesen('allVorgaben.ini', 'hochVakuum'))

    if scaleEin.get() == 0:  # Falls Schalter auf aus - Vakuumpumpe aus
        sollVakuum = 0
    # print('sollVakuum ',sollVakuum,'\tSpannung ',spannung)
    a_Interface.regler('reglerVakuum', sollVakuum)


def null_100(wert):
    if wert < 0:
        wert = 0
    elif wert > 100:
        wert = 100
    else:
        wert = wert
    return wert


def null_0(wert):
    if wert < 0:
        wert = 0
    else:
        wert = wert
    return wert

i=0
def hauptSchleife():
    global sollVL, istVL, sollRL, istRL, sollPumpe, fuellstandVL, fuellstandRL, quadFarbeVL,quadFarbeRL,i
    #print('koefVL in schleife\t', koefVL)
    istVakuum = reglerVakuumpumpe()  # Erhöht Vakuumpumpenleistung falls Dsiplay ist rot
    sollPumpe, fuellstandVL, fuellstandRL = a_Interface.fuellstandMessen(sollPumpe, statusPumpe,
                                                                       fuellstandVL, fuellstandRL)
    #print('a_Fenster: FuellstandVL', fuellstandVL,'\tFuellstandRL ', fuellstandRL)
    sollPumpe = null_100(sollPumpe)
    fuellstandVL = null_0(fuellstandVL)
    fuellstandVLAnzeige = round(fuellstandVL, 1)
    fuellstandVLTank = 100 - int(null_100(fuellstandVL))
    fuellstandRL = null_0(fuellstandRL)
    fuellstandRLAnzeige = round(fuellstandRL, 1)
    fuellstandRLTank = 100 - int(null_100(fuellstandRL))

    # istVL, istRL, istPumpe, istVakuum, istDruck, vorVakuum = istWerte()
    istVL = round(a_Interface.adc_mess('istVL'),1)
    istRL = round(a_Interface.adc_mess('istRL'),1)
    istPumpe = sollPumpe

    # Tank farbig und Werte aktualisieren-----------------------------------------------------------------
    fenster.itemconfigure(wertSollVL, text=sollVL)  # Aktualisiere Text in Textfeld
    fenster.itemconfigure(wertSollRL, text=sollRL)
    fenster.itemconfigure(wertIstVL, text=istVL)
    fenster.itemconfigure(wertIstRL, text=istRL)
    sollPumpeAnzeige = round(sollPumpe, 2)
    fenster.itemconfigure(wertPumpeIst, text=sollPumpeAnzeige)  # istPumpe zu ungenau --> sollPumpe anzeigen
    fenster.itemconfigure(wertFuellstandVL, text=fuellstandVLAnzeige)
    fenster.itemconfigure(wertFuellstandRL, text=fuellstandRLAnzeige)
    if fuellstandRL > fuellstandOEG or fuellstandRL < fuelstandUEG:
        farbeRL = 'darkred'
    else:
        farbeRL = 'darkgreen'
    dx = 50
    fenster.create_rectangle(830 + dx, 325, 980 + dx, 675, fill=farbeRL)
    fenster.create_rectangle(830 + dx, 325, 980 + dx, 325 + ((350 * fuellstandRLTank / 100)), fill=farbeTanks)

    if fuellstandVL > fuellstandOEG or fuellstandVL < fuelstandUEG:
        farbeVL = 'darkred'
    else:
        farbeVL = 'darkgreen'
    #quadFarbeRL.delete()
    i+=10
    
    quadFarbeVL=fenster.create_rectangle(450 + dx, 325, 600 + dx, 675, fill=farbeVL)
    quadFarbeRL=fenster.create_rectangle(450 + dx, 325, 600 + dx, 325 + ((350 * fuellstandVLTank / 100)), fill=farbeTanks)

    fenster.after(1000, hauptSchleife)  # reschedule event in 1 seconds


# -------------------------Start--------------------------------------------------------------------------
a_setup
a_Interface.setup(sollVL, sollRL)
hauptSchleife()
root.mainloop()
