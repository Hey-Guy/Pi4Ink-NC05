import time

import RPi.GPIO as GPIO
import requests
import smbus2 as smbus
from ads1015 import ADS1015


def encode(wert):
    hexdic = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
              'D': 13, 'E': 14, 'F': 15}
    msg = 16 * hexdic[wert[0]] + hexdic[wert[1]]
    lsg = 16 * hexdic[wert[2]] + hexdic[wert[3]]
    ergebnis = 16 * 16 * msg + lsg
    return ergebnis


def fuellstandGradient(tank: object) -> object:  # Rückgabe des Fuellstands in Einheiten des Sensors
    al1120 = '192.168.1.250'
    if 'VL' in tank:
        port = '/iolinkmaster/port[2]/iolinkdevice/pdin/getdata'
    else:
        tank = '\t\tRL'
        port = '/iolinkmaster/port[1]/iolinkdevice/pdin/getdata'
    fuellwert = requests.get('http://' + al1120 + port).json()
    fuellstr = fuellwert['data']['value']
    fuell = encode(fuellstr)

    # print('a_Extern: Tanksensor: ',tank, fuell)
    return abs(fuell)


def schalter(GIPOs, channel, wert) -> object:
    GPIO.output(GIPOs[channel], not (wert))  # False = Ein; True = Aus
    return


def setupRelais(GIPOs):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in GIPOs:
        GPIO.setup(GIPOs[pin], GPIO.OUT)
        schalter(GIPOs, pin, True)
        time.sleep(0.1)
        schalter(GIPOs, pin, False)
    return

def relaisStatus(relais):
    status=True
    if GPIO.input(relais) == GPIO.LOW:
        status = False
    return status

def setupRegler():
    i2cKanal = smbus.SMBus(1)
    i2cKanal.write_i2c_block_data(0x10, 0b00000101, [0b00000000, 0b00111111])  # pin 0 - 3 als DACs
    i2cKanal.close()


def in_MSB_LSB(wert):
    msb = int(wert / 0xFF)
    lsb = int(wert - (msb * 0xFF))
    return msb, lsb


def regler(channel, wert):  #
    DAC = {'reglerVL': 0b00010000,  # sollVL
           'reglerRL': 0b00010001,  # soolRL
           'reglerPumpe': 0b00010010,  # sollPumpe Flüssigkeit
           'reglerVakuum': 0b00010011,  # sollLeistung für Vakuumpupe
           'reglerPurgen': 0b00010100,  # Druck beim Purgen
           'messVL': 0b01000000,  # istWert Vakuum VL
           'messRL': 0b10000000}  # istWert Vakuum RL
    meldung = ''

    if (channel == 'reglerVL' or channel == 'reglerRL'):
        # wert = abs(wert)
        if wert > 100:
            wert = 100
            meldung = channel, ' mit ', wert, ' V größer als 0,5 V. Reduzierung auf 0,5V'
        elif wert < -100:
            wert = -100
        else:
            wert = wert
        signal = (0.01 * wert *4095 / 5 ) / 0.984 #0.1 von 0 bis 10 Volt bei 0 bis 1000 mbar, Korrekturfaktor 0,984
        # signal = (wertx - 1.146) / 0.0043  # Eichung Excel-Tabelle auf 0.2 mA genau
        print(channel, '\tSchieber ', wert, '\tSignalDAC ', signal)

    elif channel == 'reglerPurgen':
        wert = abs(wert)
        if wert > 0.55:
            wert = 0.55
            meldung = channel, ' mit ', wert, ' bar größer als 0.55 bar. Reduzierung auf 0.55 bar'
        elif wert < 0.0:
            wert = 0.0
        else:
            wert = wert
        # print('Sollwert ', wert)
        signal = 2803 * wert  # Eichung Excel-Tabelle y = 2803 * druck[bar]

    else:  # fuer reglerPumpe und reglerVakuum
        if wert > 95:
            wert = 95
            meldung = channel, ' mit ', wert, ' % größer als 100 %. Reduzierung auf 95 %'
        elif wert < 0:
            wert = 0
            meldung = channel, ' mit ', wert, ' kleiner als 0 %. Änderung auf 0 %'
        else:
            wert = wert
        signal = 4095 * 0.2 * wert / 20  # 0 bis 100 % auf 0 bis 5 Volt
        # print('pumpeInk\t', wert)
    # if meldung!='':
    # messagebox.showwarning('a_Extreme',meldung)
    # print(channel, '\t Vorgabe ', wert, '\tSignal ', signal, '\t', meldung)
    i2cKanal = smbus.SMBus(1)
    msb, lsb = in_MSB_LSB(signal)
    # print(channel, 'Sollwert\t',signal, '\tMSB\t', msb, ' \lsb\t', lsb)
    try:
        i2cKanal.write_i2c_block_data(0x10, DAC[channel], [msb, lsb])
    except:
        meldung = 'Schreibfehler am I2C des DAC'
        print('a_Extreme', meldung)
    i2cKanal.close()
    return


def out_MSB_LSB(msb, lsb):
    wert = msb * 255 + lsb
    return wert


def adc_mess(channel):
    DAC = {'reglerVL': 0b00010000,  # sollVL
           'reglerRL': 0b00010001,  # soolRL
           'reglerPumpe': 0b00010010,  # sollPumpe Flüssigkeit
           'reglerVakuum': 0b00010011,  # sollLeistung für Vakuumpupe
           'reglerPurgen': 0b00010100,  # Druck beim Purgen
           'messVL': 0b01000000,  # istWert Vakuum VL
           'messRL': 0b10000000}  # istWert Vakuum RL

    def adc_block_volt(wert):
        mask = 0b00001111
        msb = mask & wert[0]
        ergebnis = msb * 255 + wert[1]
        volt = ergebnis / 4095 * 5.25  # 0xFFF * 5
        return volt

    i2cKanal = SMBus(1)
    i2cPort = 0x10
    i2cKanal.write_i2c_block_data(i2cPort, 0b00000100, [0b00000000, DAC[channel]])  # pin 6 - 7 als ADCs
    i2cKanal.write_i2c_block_data(i2cPort, 0b00000010, [0b00000010, DAC[channel]])  # pin 6 - 7 als ADCs
    lesen = i2cKanal.read_i2c_block_data(i2cPort, 0b01000000, 2)
    i2cKanal.close()
    # print('Lesen\t', lesen)
    wert = adc_block_volt(lesen)
    # print('Volt\t', wert)
    return wert


def adc1015Wert(channel):
    # CHANNELS = ['in0/ref', 'in1/ref', 'in2/ref']
    ADC = {'istVL': 'in0/ref',  # istVL
           'istRL': 'in1/ref',  # istRL
           'vakuum': 'in2/ref'}  # istPumpe
    ads1015 = ADS1015()
    ads1015.set_mode('single')
    ads1015.set_programmable_gain(2.048)
    ads1015.set_sample_rate(1600)
    reference = ads1015.get_reference_voltage()
    spannung = ads1015.get_compensated_voltage(channel=ADC[channel], reference_voltage=reference)
    wert = 0
    if (channel == 'istVL' or channel == 'istRL'):
        wert = (spannung * 100)  #10 von 0 bis 10 Volt bei 0 bis 1000 mbar
    else:
        wert = spannung

    #print(channel, '\t Spannung ', spannung, '\tChannel\t', ADC[channel])
    return wert
