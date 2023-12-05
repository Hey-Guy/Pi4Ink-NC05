# für Mirkoe-2690 ADAC -Board mit Prozessor AD5593R

import smbus
from Ablage import allRelais

# Mode Bits
modBit = {'config': 0,
          'DACwrite': 0b00010000,  # DACwrite
          'ADCread': 0b01000000,  # ADCreadback
          'DACread': 0b01010000,  # DACreadback
          'GPIOread': 0b01100000,  # GPIOreadback
          'RegisterRead': 0b01110000}  # Registerreadback

# Configurationmode


register = {'ADCsequence': 0b00000010,  # ADC sequence register Selects ADCs for conversion 0x0000
            'ControlRegister': 0b00000011,  # General-purpose control register DAC and ADC control register 0x0000
            'ADC_Pin': 0b00000100,  # ADC pin configuration Selects which pins are ADC inputs 0x0000
            'DAC_Pin': 0b00000101,  # DAC pin configuration Selects which pins are DAC outputs 0x0000
            'PullDown': 0b00000110,
            # Pull-down configuration Selects which pins have an 85 kΩ pull-down resistor to GND 0x00FF
            'LoadDAC_': 0b00000111,  # LDAC mode Selects the operation of the load DAC 0x0000
            'GPIO_Pin': 0b00001000,  # GPIO write configuration Selects which pins are general-purpose outputs 0x0000
            'GPIO_Write': 0b00001001,  # GPIO write data Writes data to general-purpose outputs 0x0000
            'GPIO_Read': 0b00001010,  # GPIO read configuration Selects which pins are general-purpose inputs 0x0000
            'Power': 0b00001011,     #2,5 als Vrer: D9 = 1 --> 2,5 V an Vref
            # Power-down/reference control Powers down the DACs and enables/disables the reference 0x0000
            'GPIO_Config': 0b00001100,
            # Open-drain configuration Selects open-drain or push-pull for general-purpose outputs 0x0000
            'ThreeStatePin': 0b00001101,  # Three-state pins Selects which pins are three-stated 0x0000
            'Reset': 0b00001111}  # Software reset mit [0x0D, 0xAC]

DAC = {0: 0b00010000,  # sollVL
       1: 0b00010001,  # soolRL
       2: 0b00010010,  # sollPumpe
       3: 0b00010011,  # sollDruck
       4: 0b00010100,  # istVL
       5: 0b00010101,  # istRl
       6: 0b00010110,  # istPumpe
       7: 0b00010111}  # istDruck
# setup ADAD
i2cKanal = smbus.SMBus(1)
i2cPort = 0x10

i2cKanal.write_i2c_block_data(i2cPort, register['Reset'], [0x0D, 0xAC])
i2cKanal.write_i2c_block_data(i2cPort, register['Reset'], [0x00, 0x00])

#i2cKanal.write_i2c_block_data(i2cPort, register['ControlRegister'],[0b00000000, 0b00000000])  # ADC und DAC auf 2 x Vref
i2cKanal.write_i2c_block_data(i2cPort, register['DAC_Pin'], [0b00000000, 0b00001111])  # pin 0 - 3 als DACs


'''
reg = i2cKanal.read_i2c_block_data(i2cPort,modBit['RegisterRead']|register['ADC_Pin'],2)
print('reg ',reg)
i2cKanal.write_i2c_block_data(i2cPort, register['ADC_Pin'], [0b00000000, 0b10000000])  # pin 4 - 7 als DACs
reg = i2cKanal.read_i2c_block_data(i2cPort,modBit['RegisterRead']|register['ADC_Pin'],2)
print('reg - neu',reg)

reg = i2cKanal.read_i2c_block_data(i2cPort,modBit['ADCread'])
print('reg - wert',reg)

#msg2 = i2cKanal.write_i2c_block_data(i2cPort, DAC[7], [0b10000000, 0b0])
#msg2 = i2cKanal.write_i2c_block_data(i2cPort, DAC[7], [0b10001111, 0b11111111])
#msg2 = i2cKanal.read_i2c_block_data(i2cPort, register['ControlRegister'])
#print(msg2)
'''

def in_MSB_LSB(wert):
    msb = int(wert / 0xFF)
    lsb = int(wert - (msb * 0xFF))
    return msb, lsb


def von_MSB_LSB(msb, lsb):
    wert = msb * 0xFF + lsb
    return wert


def dac(chanel, volt):  # wert 0 - 10 V
    signal = volt * 4095 * 0.2  #
    msb, lsb = in_MSB_LSB(signal)
    i2cKanal.write_i2c_block_data(i2cPort, DAC[chanel], [msb, lsb])
    signal = i2cKanal.read_word_data(i2cPort, DAC[chanel])
    print(in_MSB_LSB(signal))
    return


def adc(pin,wert):

    i2cKanal.write_i2c_block_data(i2cPort, 0b00000100, [0b00000000, pin])  # pin 7 als ADCs
    #i2cKanal.write_i2c_block_data(i2cPort, 0b00000010, [0b00000010, pin])  # Conversion

    signal = i2cKanal.read_word_data(i2cPort,0b000000010)
    print('ADC ',wert, ' ',signal)
    volt = 0
    signal = 0
    # volt = 10* (signal[0] * 0xFF + signal[1]) / 4095
    volt = signal / 4095
    return volt

allRelais.setup()
allRelais.startAuto(0, 0)

dac(0, 1)   #VL
dac(1, 2)   #RL
dac(2, 3)     #Pumpe   12 cm Höhenunterschied ca. 2.5 V
dac(3, 4)     #Vakuum

#allRelais.stoppAuto()
'''
for i in range(0,1):
    wert= i*0.1
    dac(2,wert)
    time.sleep(1)
    adc(0b10000001,wert)
'''
i2cKanal.close()
