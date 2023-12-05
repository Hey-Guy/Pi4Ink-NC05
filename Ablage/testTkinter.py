from tkinter import *
import basics
from random import *

wert = DoubleVar

grundflaeche = Tk()
grundflaeche.title('testTkinter')
grundflaeche.geometry('300x300+400+50')
zeichenFlaeche = Canvas(grundflaeche, bd=0, width=300, height=300)
zeichenFlaeche.pack()

istRL = DoubleVar()
istRL= 1.2

zeichenFlaeche.create_text(100,100, text='mbar Istwert',)
labelIstRL = zeichenFlaeche.create_text(50,50, text=istRL,)
labelIstRL2 = zeichenFlaeche.create_text(100,50, text=istRL,)

def task():
    global wert
    wert=randint(0,100)
    zeichenFlaeche.itemconfigure(labelIstRL, text=wert)

    print(wert)
    grundflaeche.after(1000, task)  # reschedule event in 1 seconds

#task()



#grundflaeche.after(1000, task())

grundflaeche.mainloop()