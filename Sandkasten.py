import basics


def fuellstandNormierungSchritte(fuellsensor, tank):  # Linear zwischen 0 und 20% und 20% bis 100% -2 Geraden
    stufen = [0, 10, 20, 30, 40, 50, 99]  # zweimal 99, wegen Überlauf variable
    fuellEichung = []
    for i in stufen:
        titel = tank + str(i)
        fuellEichung.append(float(basics.iniLesen('allVorgaben.ini', titel)))
    schritteLen = len(stufen)-1
    if fuellsensor >= fuellEichung[schritteLen]:
        m = (stufen[schritteLen] - stufen[schritteLen-1]) / (fuellEichung[schritteLen] - fuellEichung[schritteLen-1])
        t = stufen[schritteLen] - m * fuellEichung[schritteLen]
    else:
        for i in range(0,schritteLen):
            if fuellsensor < fuellEichung[i + 1]:
                m = (stufen[i + 1] - stufen[i]) / (fuellEichung[i + 1] - fuellEichung[i])
                t = stufen[i] - m * fuellEichung[i]
                break
    fuellProzent = m * fuellsensor + t
    if fuellProzent < 0:
        fuellProzent=0
    print('a_Interface m ', m, '\t t', t, '\tfuellProzent', fuellProzent ,'fuellEichung', fuellEichung)
    return


fuellstandNormierungSchritte(500, 'VL', )
