import sys
def iniLesen(datei, einstellung):
    try:
        inhaltIni = open(datei, 'r')
    except Exception:
        # print(os.path.dirname(os.path.abspath(__file__)))
        return -99

    gefunden = False
    inhalt = '-1'
    for i, zeile in enumerate(inhaltIni):
        if gefunden:
            inhalt = zeile.replace('\n', '')
            break
        if einstellung in zeile:
            gefunden = True

    inhaltIni.close()
    if not (gefunden):
        print('Fehler - Lesen: ', datei, einstellung, '\tWert ', inhalt, '\tWert ', gefunden, sys.path)
    return inhalt


def iniSchreiben(datei, einstellung, wert) -> object:
    try:
        inhaltIni = open(datei, 'r')
    except Exception:
        # print(os.path.dirname(os.path.abspath(__file__)))
        return 0
    inhaltListe = inhaltIni.readlines()
    inhaltIni.close()

    gefunden = False
    gefundenGlobal = False
    inhaltIni = open(datei, 'w')
    for i, zeile in enumerate(inhaltListe):
        if gefunden:
            inhaltIni.write(str(wert) + '\n')
            # print('iniSchreiben ',  datei, einstellung, wert)
            gefunden = False
        else:
            inhaltIni.write(zeile)
        if einstellung in zeile:
            gefunden = True
            gefundenGlobal = True
    if not (gefundenGlobal):
        print('basics: Fehler - Schreiben: ', datei, einstellung, wert, gefunden)
    inhaltIni.close()
    return 1
