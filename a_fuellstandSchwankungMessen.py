import sys
from datetime import datetime

if '/usr/bin' in sys.executable:  # Auswhal, ob python am Pi oder am LapTop
    import a_Extern as ziel
else:
    import a_Intern as ziel

import a_Interface

dateiname = 'fuellstand-2.txt'
datei = open(dateiname, 'w')
datei.write('Zeit,VL,RL')
datei.close

datei = open(dateiname, 'a')
for i in range(100):
    fuellVLsensor = ziel.fuellstandGradient('VL')
    fuellRLsensor = ziel.fuellstandGradient('RL')
    datei.write('\n' + str(fuellVLsensor) + '\t' + str(fuellRLsensor))


datei.close

datei = open(dateiname,'r')
print(datei.read())
datei.close
