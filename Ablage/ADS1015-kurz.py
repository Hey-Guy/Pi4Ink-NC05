from ads1015 import ADS1015
import time

def ads1015Wert(channel):
    CHANNELS = ['in0/ref', 'in1/ref', 'in2/ref']
    ads1015 = ADS1015()
    ads1015.set_mode('single')
    ads1015.set_programmable_gain(2.048)
    ads1015.set_sample_rate(1600)
    reference = ads1015.get_reference_voltage()
    #print("Reference voltage: {:6.3f}v \n".format(reference))
    wert = ads1015.get_compensated_voltage(channel=CHANNELS[channel], reference_voltage=reference)
    return wert


while True:
    for channel in range(2,3):
        wert = ads1015Wert(channel)
        print("{}: {:6.3f}v".format(channel, wert))
    time.sleep(1)
    #print('')