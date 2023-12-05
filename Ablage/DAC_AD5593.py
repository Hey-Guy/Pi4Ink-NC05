from smbus2 import SMBus

print('Skript DAC_AD5593.py -----------------------')

def in_MSB_LSB(wert):
    msb = int(wert / 0xFF)
    lsb = int(wert - (msb * 0xFF))
    return msb, lsb

def out_MSB_LSB(msb, lsb):
    wert = msb * 255 + lsb
    return wert

def adc_mess(channel):
    DAC = {'reglerVL': 0b00010000,  # sollVL
           'reglerRL': 0b00010001,  # soolRL
           'reglerPumpe': 0b00010010,  # sollPumpe Flüssigkeit
           'reglerVakuum': 0b00010011,  # sollLeistung für Vakuumpupe
           'reglerPurgen': 0b00010100,  # Druck beim Purgen
            'messVL': 0b01000000,      #istWert Vakuum VL
            'messRL': 0b10000000}      #istWert Vakuum RL

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
    lesen =i2cKanal.read_i2c_block_data(i2cPort,0b01000000,2)
    i2cKanal.close()
    print('Lesen\t',lesen)
    wert = adc_block_volt(lesen)
    print('Volt\t',wert)

adc_mess('messRL')
adc_mess('messVL')

#regler('reglerVL',1)
'''regler('reglerRL',10)
regler('reglerPumpe',100)
regler('reglerVakuum',0)'''
print('Fertig')




#Wert in mA (zwischen 4 und 20 --> 0,0005 bis - 0,1 bar)