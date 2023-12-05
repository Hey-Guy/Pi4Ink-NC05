#import RPi.GPIO as PWM
#from ads1015 import ADS1015

def vakuumventile(nummer, zustand):
    return

def druckluftventil(zustand):
    return

def druckLos(zustand):
    return

def reglerVLDef(wert):

    return

def pumpeDef(wert) -> object:
    return

def dac(kanal, wert):
    '''i2c = board.I2C()  # uses board.SCL and board.SDA
    mcp4728 = adafruit_mcp4728.MCP4728(i2c)
    antwort = ''
    if kanal == 'a':
        if wert == 0:
            mcp4728.channel_a.value = 0
        else:
            mcp4728.channel_a.value = int(65535 / wert)  # Voltage = VDD/wert
    elif kanal == '':
        if wert == 0:
            mcp4728.channel_b.value = 0
        else:
            mcp4728.channel_b.value = int(65535 / wert)
    elif kanal == '':
        if wert == 0:
            mcp4728.channel_c.value = 0
        else:
            mcp4728.channel_c.value = int(65535 / wert)
    elif kanal == '':
        if wert == 0:
            mcp4728.channel_d.value = 0
        else:
            mcp4728.channel_d.value = int(65535 / wert)
    else:
        antwort = '-1'

    mcp4728.save_settings()  # save
    return antwort
    '''

def adc(kanal):
    '''value = ''

    ads1015 = ADS1015()
    chip_type = ads1015.detect_chip_type()
    ads1015.set_mode('single')
    ads1015.set_programmable_gain(2.048)

    if chip_type == 'ADS1015':
        ads1015.set_sample_rate(1600)
    else:
        ads1015.set_sample_rate(860)

    reference = ads1015.get_reference_voltage()

    if reference != 0:
        channel = 'in' + str(kanal) + '/ref'
        value = ads1015.get_compensated_voltage(channel=channel, reference_voltage=reference)
    else:
        value = 'kein Wert'
    return value
    '''

#dac(0,5)