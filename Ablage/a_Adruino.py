import time

import smbus2 as smbus


def out_MSB_LSB(msb, lsb):
    wert = msb * 255 + lsb
    return wert


def arduino():
    i2cKanal = smbus.SMBus(1)
    istVL = -1
    istRL = -1
    istPumpe = -1
    istVakuum = -1
    istDruck = -1
    vorVakuum = -1

    #time.sleep(1)
    try:
        data = i2cKanal.read_i2c_block_data(0x40, 0, 12)
        istVL = out_MSB_LSB(data[0], data[1]) * 5 / 1024  # in Volt der Eingangsspannung
        istRL = out_MSB_LSB(data[2], data[3])  # in Volt der Eingangsspannung
        istPumpe = out_MSB_LSB(data[4], data[5])
        istVakuum = out_MSB_LSB(data[6], data[7])
        istDruck = out_MSB_LSB(data[8], data[9]) * 5 / 1024  # in Volt der Eingangsspannung
        vorVakuum = out_MSB_LSB(data[10], data[11]) * 5 / 1024  # in Volt der Eingangsspannung
        # print(data)


    except:
        print("I2C - Arduino Fehler in def arduino():")
        # time.sleep(1)
    print('Ist - VL ', istVL, '\tRL ', istRL, '\tPumpe ', istPumpe, '\tVakuum ', istVakuum, '\tDruck ',
          istDruck, '\tvorVakuum ', vorVakuum)
    i2cKanal.close()

    return istVL, istRL, istPumpe, istVakuum, istDruck, vorVakuum

while True:
    arduino()
